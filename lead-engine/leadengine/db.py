"""SQLite storage for the lead engine.

One file (instance/leads.db by default, override with LEADENGINE_DB). Every fact the
system knows about a lead is stored with its source, so profiles and summaries are
traceable and so contact details can prove their Spam Act basis.
"""
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "instance" / "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL DEFAULT 'business',      -- business | owner
    display_name TEXT NOT NULL,                 -- how we refer to them internally
    trading_name TEXT,                          -- brand they trade under
    registered_name TEXT,                       -- ABR entity / registered business name
    abn TEXT, entity_type TEXT, abn_status TEXT, gst_registered TEXT,
    abn_state TEXT, abn_postcode TEXT,
    website TEXT, business_type TEXT, office_suburb TEXT,
    group_name TEXT,
    airbnb_host_id TEXT UNIQUE,
    listings_active INTEGER DEFAULT 0, houses INTEGER DEFAULT 0, units INTEGER DEFAULT 0,
    top_suburbs TEXT,
    angle TEXT,                                 -- A / B / C pitch
    hook TEXT,                                  -- one-sentence personalised opener
    no_marketing_notice TEXT DEFAULT 'unknown', -- yes | no | unknown
    status TEXT NOT NULL DEFAULT 'new',
    notes TEXT,
    source TEXT,
    created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    name TEXT, role TEXT, email TEXT, phone TEXT,
    basis TEXT NOT NULL,          -- published_business | consent | referral
    source_url TEXT,              -- where a published contact was found
    consent_text TEXT, consent_at TEXT,
    is_primary INTEGER DEFAULT 0,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL,
    address TEXT NOT NULL, suburb TEXT,
    lat REAL, lng REAL, hex TEXT,
    kind TEXT,                    -- house | unit | complex | unknown
    signal TEXT,                  -- short_term_accommodation | dual_occupancy | secondary_dwelling | owner_provided
    da_ram_id TEXT, da_use TEXT, da_date TEXT, da_status TEXT,
    hex_active_listings INTEGER, hex_self_managed_houses INTEGER,
    collection_day TEXT,
    status TEXT NOT NULL DEFAULT 'new',   -- new | letter_queued | letter_sent | responded | customer | do_not_contact
    notes TEXT,
    created_at TEXT, updated_at TEXT,
    UNIQUE(address, signal)
);
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    topic TEXT,                   -- portfolio | services | registration | web | planning | market | note
    fact TEXT NOT NULL,
    source_name TEXT, source_url TEXT,
    collected_at TEXT,
    UNIQUE(account_id, property_id, fact)
);
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    text TEXT NOT NULL, generated_by TEXT, generated_at TEXT
);
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    audience TEXT NOT NULL DEFAULT 'business',   -- business | owner | property_letter
    angle TEXT, channel TEXT NOT NULL DEFAULT 'email',
    subject TEXT, body TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS drafts (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE SET NULL,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES templates(id) ON DELETE SET NULL,
    channel TEXT NOT NULL DEFAULT 'email',
    to_address TEXT, subject TEXT, body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',  -- draft | approved | sent | exported | failed | cancelled
    compliance TEXT,                       -- JSON {errors:[], warnings:[]}
    provider TEXT, provider_ref TEXT, error TEXT,
    created_at TEXT, approved_at TEXT, sent_at TEXT
);
CREATE TABLE IF NOT EXISTS touches (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    happened_at TEXT, channel TEXT, outcome TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS suppression (
    id INTEGER PRIMARY KEY,
    value TEXT UNIQUE NOT NULL,   -- email, @domain, phone digits, or address
    reason TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""

DEFAULT_SETTINGS = {
    "sender_name": "[Your name]",
    "sender_role": "Business Development",
    "business_name": "Bin Caddie Property Services",
    "business_phone": "0418 475 510",
    "business_email": "admin@bincaddie.com.au",
    "business_website": "bincaddie.com.au",
    "business_abn": "39 174 579 656",
    "business_location": "Sunshine Coast QLD",
    "offer_price": "$80 per home per month (ex GST)",
    "offer_trial": "a free 2-week trial on 3-5 homes",
    "email_provider": "outbox",       # outbox | smtp | gmail | outlook
    "daily_send_cap": "20",
    "smtp_host": "", "smtp_port": "587", "smtp_username": "", "smtp_from": "",
    "abr_guid": "",
    "llm_enabled": "auto",            # auto | on | off
    "llm_model": "",                 # Claude model ID; or set LEADENGINE_LLM_MODEL
}

ACCOUNT_STATUSES = ["new", "researched", "ready", "contacted", "replied", "meeting",
                    "pilot", "customer", "not_interested", "do_not_contact"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db_path() -> Path:
    return Path(os.environ.get("LEADENGINE_DB", DEFAULT_DB))


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = path or db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def session(path: Path | None = None):
    conn = connect(path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    for k, v in DEFAULT_SETTINGS.items():
        conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)", (k, v))
    from .seed_templates import seed
    seed(conn)


def settings(conn: sqlite3.Connection) -> dict:
    s = dict(DEFAULT_SETTINGS)
    s.update({r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM settings")})
    return s


def set_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute("INSERT INTO settings(key, value) VALUES (?, ?) "
                 "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))


def add_fact(conn, fact: str, *, account_id=None, property_id=None, topic="note",
             source_name=None, source_url=None) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO facts(account_id, property_id, topic, fact, source_name, source_url, collected_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (account_id, property_id, topic, fact.strip(), source_name, source_url, now()),
    )


def upsert_contact(conn, account_id: int, *, email=None, phone=None, name=None, role=None,
                   basis="published_business", source_url=None, consent_text=None,
                   is_primary=0) -> int:
    """Add a contact unless the same email (or phone, when no email) already exists for the account."""
    key_col, key_val = ("email", email) if email else ("phone", phone)
    if key_val:
        row = conn.execute(f"SELECT id FROM contacts WHERE account_id = ? AND {key_col} = ?",
                           (account_id, key_val)).fetchone()
        if row:
            conn.execute("UPDATE contacts SET name = COALESCE(?, name), role = COALESCE(?, role), "
                         "source_url = COALESCE(?, source_url) WHERE id = ?",
                         (name, role, source_url, row["id"]))
            return row["id"]
    cur = conn.execute(
        "INSERT INTO contacts(account_id, name, role, email, phone, basis, source_url, consent_text, "
        "consent_at, is_primary, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (account_id, name, role, email, phone, basis, source_url, consent_text,
         now() if basis == "consent" else None, is_primary, now()),
    )
    return cur.lastrowid


def as_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)
