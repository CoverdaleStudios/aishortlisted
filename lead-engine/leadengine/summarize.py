"""Profile summaries and personalised one-line hooks.

Always works offline (a plain-English summary assembled from stored facts). If Claude API
credentials are available and LLM use is on, Claude writes a sharper brief and an opening
hook - using ONLY the stored facts, which are passed with their sources.
"""
import os
import re

from . import db

SYSTEM = (
    "You write internal sales briefs for Bin Caddie, a Sunshine Coast (Queensland) business that puts "
    "holiday-rental wheelie bins out before council collection and back in after, twice a week, with "
    "time-stamped photo proof ($80/month ex GST per home, no lock-in), plus bin cleaning and bin-room "
    "service for complexes. Use only the facts provided. Never invent names, numbers or claims. If a fact "
    "is missing, leave it out. Never suggest contacting private individuals or mentioning that we noticed "
    "their bins."
)


def facts_for(conn, account_id=None, property_id=None):
    if account_id:
        return conn.execute("SELECT * FROM facts WHERE account_id = ? ORDER BY topic, id", (account_id,)).fetchall()
    return conn.execute("SELECT * FROM facts WHERE property_id = ? ORDER BY topic, id", (property_id,)).fetchall()


def plain_summary(account, facts) -> str:
    a = account
    lines = [f"{a['trading_name'] or a['display_name']}"
             + (f" (registered: {a['registered_name']}, ABN {a['abn']})" if a["registered_name"] else "")
             + (f" - {a['business_type']}" if a["business_type"] else "")
             + (f", office in {a['office_suburb']}" if a["office_suburb"] else "") + "."]
    if a["listings_active"]:
        lines.append(f"Portfolio: {a['listings_active']} active short-stay listings "
                     f"({a['houses']} houses, {a['units']} units), mainly {a['top_suburbs']}.")
    if a["group_name"]:
        lines.append(f"Part of {a['group_name']} - pitch at group level once.")
    pitch = {"A": "Angle A (guest bins nobody owns) - house-heavy portfolio.",
             "B": "Angle B (Noosa contact person) - Noosa short-stay manager.",
             "C": "Angle C (owner-services add-on / bin rooms) - unit-heavy portfolio."}.get(a["angle"] or "")
    if pitch:
        lines.append(pitch)
    for f in facts:
        if f["topic"] in ("services", "research", "registration", "web"):
            lines.append(f"- {f['fact']}")
    return "\n".join(lines)


def property_summary(prop, facts) -> str:
    lines = [f"{prop['address']} - {prop['kind']} flagged by {prop['signal'].replace('_', ' ')}."]
    lines += [f"- {f['fact']}" for f in facts]
    lines.append("Contact route: letter addressed to 'The Owner' (no personal details held).")
    return "\n".join(lines)


def _model(settings: dict) -> str:
    return (settings.get("llm_model") or os.environ.get("LEADENGINE_LLM_MODEL", "")).strip()


def llm_available(settings: dict) -> bool:
    mode = settings.get("llm_enabled", "auto")
    if mode == "off" or not _model(settings):
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    if mode == "on":
        return True
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def _claude(settings: dict, prompt: str, max_tokens: int = 2000) -> str:
    import anthropic

    client = anthropic.Anthropic()
    try:
        resp = client.beta.messages.create(
            model=_model(settings),
            max_tokens=max_tokens,
            system=SYSTEM,
            output_config={"effort": "low"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.RateLimitError as e:
        raise RuntimeError("Claude API rate limit - try again shortly.") from e
    except anthropic.APIStatusError as e:
        raise RuntimeError(f"Claude API error {e.status_code}: {e.message}") from e
    except anthropic.APIConnectionError as e:
        raise RuntimeError("Could not reach the Claude API.") from e
    if resp.stop_reason == "refusal":
        raise RuntimeError("Claude declined this request.")
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _facts_block(facts) -> str:
    return "\n".join(f"- [{f['topic']}] {f['fact']} (source: {f['source_name'] or 'n/a'})" for f in facts)


def summarize_account(conn, account, settings: dict) -> str:
    facts = facts_for(conn, account_id=account["id"])
    base = plain_summary(account, facts)
    if not llm_available(settings):
        text, by = base, "rules"
    else:
        prompt = (f"Account record:\n{base}\n\nAll stored facts:\n{_facts_block(facts)}\n\n"
                  "Write a brief for the salesperson (max 150 words): who they are, portfolio shape and where, "
                  "what they already handle for owners, the most likely bin-related pain point, and the single "
                  "best opening angle. Plain text, no headings.")
        text, by = _claude(settings, prompt), _model(settings)
    conn.execute("INSERT INTO summaries(account_id, text, generated_by, generated_at) VALUES (?, ?, ?, ?)",
                 (account["id"], text, by, db.now()))
    return text


def _rule_hook(account, facts) -> str:
    """Offline fallback: pick the most specific true thing we know, most specific first."""
    # Only facts about THEM - 'research' facts are our own pitch notes and would echo back.
    text = " ".join(f["fact"] for f in facts if f["topic"] in ("services", "portfolio", "web")).lower()
    contractors = [w for w in ("pool", "garden", "pest", "linen", "maintenance") if w in text]
    if "non-serviced" in text:
        return "Your site mentions your rentals are non-serviced, which usually means nobody is on site on bin night."
    if "no lock-in" in text or "no lock in" in text:
        return "Like your no-lock-in owner agreements, our service doesn't lock anyone in either."
    if re.search(r"photo[- ]evidence|photo[- ]evidenced|photo report", text):
        return "Your cleans are built on photo evidence, and so is everything we do."
    if len(contractors) >= 2:
        return (f"I saw you already arrange {', '.join(contractors[:-1])} and {contractors[-1]} for owners. "
                "Bins are usually the one job left over.")
    if account["group_name"] and account["group_name"].lower() not in (account["display_name"] or "").lower():
        return f"I understand you're part of {account['group_name']}, so this could work across the group's coastal brands."
    return ""  # templates already name their suburbs; a vague hook is worse than none


def write_hook(conn, account, settings: dict) -> str:
    """One sentence that opens the email, grounded in a public fact about their business."""
    facts = facts_for(conn, account_id=account["id"])
    if llm_available(settings):
        prompt = (f"Business: {account['trading_name'] or account['display_name']}\n"
                  f"Facts:\n{_facts_block(facts)}\n\n"
                  "Write ONE friendly, specific opening sentence (max 30 words) for a cold email to this "
                  "business, referring to something true from the facts about how they look after owners or "
                  "guests (e.g. services they already arrange, their area). No flattery, no questions about "
                  "bins yet, no numbers unless given. Output only the sentence.")
        hook = _claude(settings, prompt, max_tokens=1000).splitlines()[0].strip().strip('"')
    else:
        hook = _rule_hook(account, facts)
    conn.execute("UPDATE accounts SET hook = ?, updated_at = ? WHERE id = ?", (hook, db.now(), account["id"]))
    return hook
