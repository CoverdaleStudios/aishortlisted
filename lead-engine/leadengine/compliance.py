"""Compliance gate. A draft with any error cannot be approved or sent.

Encodes the rules from the research (general information, not legal advice):
- Spam Act 2003: email only to (a) a business address the business itself publishes, where the
  message relates to the recipient's role and there's no 'no marketing' notice (inferred consent
  by conspicuous publication), or (b) someone who gave express consent. Identify the sender,
  include a functional unsubscribe, honour opt-outs.
- Never email private individuals who haven't opted in (e.g. owners found via council data).
- Do Not Call / Telemarketing Standard: call windows for phone tasks.
"""
import re
from datetime import datetime
from zoneinfo import ZoneInfo

BRISBANE = ZoneInfo("Australia/Brisbane")
FREE_MAIL = {"gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "yahoo.com.au", "bigpond.com",
             "bigpond.net.au", "icloud.com", "live.com", "live.com.au", "optusnet.com.au", "me.com"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_suppressed(conn, email: str | None = None, phone: str | None = None, address: str | None = None) -> bool:
    values = []
    if email:
        e = email.strip().lower()
        values += [e, "@" + e.split("@")[-1]]
    if phone:
        values.append(re.sub(r"\D", "", phone))
    if address:
        values.append(address.strip().lower())
    if not values:
        return False
    q = "SELECT 1 FROM suppression WHERE lower(value) IN (%s) LIMIT 1" % ",".join("?" * len(values))
    return conn.execute(q, values).fetchone() is not None


def check_email(conn, settings: dict, account, contact, body: str, sent_today: int) -> dict:
    errors, warnings = [], []
    if account is None or contact is None:
        return {"errors": ["Email drafts need an account and a contact."], "warnings": []}
    email = (contact["email"] or "").strip()
    if not EMAIL_RE.match(email):
        errors.append("Contact has no valid email address.")
    if account["status"] == "do_not_contact":
        errors.append("Account is marked do-not-contact.")
    if (account["no_marketing_notice"] or "").lower() == "yes":
        errors.append("The source page carries a 'no marketing' notice - inferred consent does not apply.")
    if email and is_suppressed(conn, email=email):
        errors.append("Address or domain is on the suppression list.")

    basis = contact["basis"]
    if account["kind"] == "owner" and basis not in ("consent", "referral"):
        errors.append("Private owners can only be emailed after they opt in (consent) - use a letter instead.")
    if basis == "published_business":
        if not contact["source_url"]:
            errors.append("Published-business basis needs the source URL where the address is published.")
        if email and email.split("@")[-1].lower() in FREE_MAIL:
            warnings.append("Free webmail address - confirm it is published as the business's address, not a personal one.")
        if account["kind"] != "business":
            errors.append("Published-business basis only applies to business accounts.")
    elif basis == "consent":
        if not contact["consent_at"]:
            errors.append("Consent basis but no consent timestamp recorded.")
    elif basis == "referral":
        warnings.append("Referral basis: make sure the person agreed to be introduced before emailing.")
    else:
        errors.append(f"Unknown contact basis '{basis}'.")

    if "unsubscribe" not in body.lower():
        errors.append("Body has no unsubscribe instruction.")
    if settings["business_abn"] not in body and settings["business_name"] not in body:
        errors.append("Body does not identify the sender business.")
    if re.search(r"\[[A-Z][^\]]{2,}\]", body):
        errors.append("Body still contains a [PLACEHOLDER].")
    if "left out" in body.lower() and "bin" in body.lower() and account["kind"] == "owner":
        warnings.append("Avoid telling owners we noticed their bins - it reads as surveillance.")
    cap = int(settings.get("daily_send_cap") or 20)
    if sent_today >= cap:
        errors.append(f"Daily send cap reached ({cap}). Raise it in Settings or send tomorrow.")
    return {"errors": errors, "warnings": warnings}


def check_letter(conn, prop) -> dict:
    errors = []
    if prop is None:
        return {"errors": ["Letters need a property."], "warnings": []}
    if prop["status"] == "do_not_contact" or is_suppressed(conn, address=prop["address"]):
        errors.append("Address is on the suppression list.")
    return {"errors": errors, "warnings": []}


def call_window(at: datetime | None = None) -> tuple[bool, str]:
    """Telemarketing Standard calling hours (Brisbane time). Public holidays: check manually."""
    t = (at or datetime.now(BRISBANE)).astimezone(BRISBANE)
    wd, h = t.weekday(), t.hour + t.minute / 60
    if wd == 6:
        return False, "No telemarketing calls on Sundays."
    if wd == 5:
        ok = 9 <= h < 17
        return ok, "Saturday window is 9am-5pm." if not ok else "OK (Saturday 9am-5pm)."
    ok = 9 <= h < 20
    return ok, "Weekday window is 9am-8pm." if not ok else "OK (weekday 9am-8pm)."
