"""Render personalised messages from templates + what the database knows about a lead."""
import re

from jinja2 import StrictUndefined, TemplateError
from jinja2.sandbox import SandboxedEnvironment

ENV = SandboxedEnvironment(undefined=StrictUndefined, autoescape=False, trim_blocks=False)


def _first_name(name: str | None) -> str | None:
    if not name:
        return None
    part = re.split(r"\s+", name.strip())[0]
    return part if part and part[0].isalpha() else None


def sender_ctx(s: dict) -> dict:
    return {
        "name": s["sender_name"], "role": s["sender_role"], "business": s["business_name"],
        "business_short": s["business_name"].replace(" Property Services", ""),
        "phone": s["business_phone"], "email": s["business_email"],
        "website": s["business_website"], "abn": s["business_abn"], "location": s["business_location"],
    }


def footer(s: dict) -> str:
    """Spam Act: identify the sender and give a functional way to opt out - on every email."""
    return (
        f"\n\n--\n{s['sender_name']}, {s['sender_role']} | {s['business_name']}\n"
        f"{s['business_phone']} | {s['business_email']} | {s['business_website']}\n"
        f"ABN {s['business_abn']} | {s['business_location']}\n"
        "Not relevant to you? Reply \"unsubscribe\" and we won't contact you again."
    )


def context_for(settings: dict, account=None, contact=None, prop=None, extra=None) -> dict:
    a = dict(account) if account else {}
    c = dict(contact) if contact else {}
    p = dict(prop) if prop else {}
    suburbs = [re.sub(r"\s*\(\d+\)$", "", x).strip() for x in (a.get("top_suburbs") or "").split(";") if x.strip()]
    suburbs = [x.split(" - ")[0] for x in suburbs]
    trading = a.get("trading_name") or a.get("display_name") or ""
    first = _first_name(c.get("name"))
    ctx = {
        "account": {
            "display_name": a.get("display_name", ""), "trading_name": trading,
            "registered_name": a.get("registered_name") or trading, "abn": a.get("abn") or "",
            "office_suburb": a.get("office_suburb") or "",
        },
        "contact": {"name": c.get("name") or "", "first_name": first or "", "role": c.get("role") or ""},
        "greeting_name": first or (f"{trading} team" if trading else "there"),
        "portfolio": {
            "listings": a.get("listings_active") or 0, "houses": a.get("houses") or 0,
            "units": a.get("units") or 0,
            "first_suburb": suburbs[0] if suburbs else "",
            "suburbs": " and ".join(suburbs[:2]) if suburbs else "",
        },
        "hook": (a.get("hook") or "").strip(),
        "property": {
            "address": p.get("address") or "", "suburb": p.get("suburb") or "",
            "collection_day": p.get("collection_day") or "",
        },
        "sender": sender_ctx(settings),
        "offer": {"price": settings["offer_price"], "trial": settings["offer_trial"]},
        "letter_code": f"OWN{p['id']}" if p.get("id") else "OWN",
    }
    if extra:
        ctx.update(extra)
    return ctx


def render(template, ctx: dict, settings: dict) -> tuple[str, str, list[str]]:
    """Return (subject, body, problems). Missing merge fields are reported, not silently blanked."""
    problems = []
    try:
        subject = ENV.from_string(template["subject"] or "").render(**ctx).strip()
        body = ENV.from_string(template["body"]).render(**ctx).strip()
    except TemplateError as e:
        return "", "", [f"Template error: {e}"]
    body = re.sub(r"\n{3,}", "\n\n", body)
    if "[" in body and "]" in body and re.search(r"\[[A-Z][^\]]{2,}\]", body):
        problems.append("Body still contains a [PLACEHOLDER] - fill it in before approving.")
    if template["channel"] == "email":
        body += footer(settings)
    return subject, body, problems
