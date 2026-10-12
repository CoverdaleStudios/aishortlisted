"""End-to-end checks: import -> profile -> compose -> compliance gate -> outbox export."""
import os
import re
from pathlib import Path

import pytest

PHASE0 = Path(__file__).resolve().parents[2] / "bin-caddie-phase0" / "outputs" / "hosts_ranked.csv"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LEADENGINE_DB", str(tmp_path / "t.db"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from leadengine.mail import providers
    monkeypatch.setattr(providers, "EXPORTS", tmp_path / "outbox")
    from leadengine.app import create_app
    app = create_app(tmp_path / "t.db")
    app.config["TESTING"] = True
    from leadengine import db
    with db.session(tmp_path / "t.db") as conn:
        db.set_setting(conn, "sender_name", "Test Sender")
    return app.test_client()


def _db(tmp_path):
    from leadengine import db
    return db.connect(tmp_path / "t.db")


def _business(conn, email="info@example-holidays.com.au", source="https://example-holidays.com.au/contact",
              kind="business", basis="published_business"):
    from leadengine import db
    cur = conn.execute("INSERT INTO accounts(kind, display_name, trading_name, listings_active, houses, units, "
                       "top_suburbs, angle, status) VALUES (?, 'Example Holidays', 'Example Holidays', 20, 12, 8, "
                       "'Coolum Beach (12); Marcoola - Mudjimba (8)', 'A', 'researched')", (kind,))
    aid = cur.lastrowid
    cid = db.upsert_contact(conn, aid, email=email, name="Jo Citizen", role="Operations Manager", basis=basis,
                            source_url=source, consent_text="yes" if basis == "consent" else None, is_primary=1)
    conn.commit()
    return aid, cid


def test_placeholder_sender_blocks(tmp_path, monkeypatch):
    from leadengine import compliance, db
    conn = db.connect(tmp_path / "p.db")
    db.init(conn)
    aid, cid = _business(conn)
    a = conn.execute("SELECT * FROM accounts WHERE id = ?", (aid,)).fetchone()
    c = conn.execute("SELECT * FROM contacts WHERE id = ?", (cid,)).fetchone()
    s = db.settings(conn)  # default sender_name is "[Your name]"
    rep = compliance.check_email(conn, s, a, c, "Hi\n[Your name]\nunsubscribe " + s["business_abn"], 0)
    assert any("PLACEHOLDER" in e for e in rep["errors"])


def test_pages_render(client):
    for url in ["/", "/accounts", "/properties", "/outbox", "/templates", "/suppression", "/settings", "/capture", "/bulk"]:
        assert client.get(url).status_code == 200, url


def test_compose_approve_export(client, tmp_path):
    conn = _db(tmp_path)
    aid, cid = _business(conn)
    tid = conn.execute("SELECT id FROM templates WHERE name LIKE 'A1%'").fetchone()[0]
    r = client.get(f"/accounts/{aid}/compose?template_id={tid}&contact_id={cid}")
    html = r.get_data(as_text=True)
    assert "Hi Jo," in html and "Coolum Beach" in html and "unsubscribe" in html
    r = client.post(f"/accounts/{aid}/compose", data={"template_id": tid, "contact_id": cid})
    did = int(re.search(r"/drafts/(\d+)", r.headers["Location"]).group(1))
    client.post(f"/drafts/{did}/approve")
    assert conn.execute("SELECT status FROM drafts WHERE id = ?", (did,)).fetchone()[0] == "approved"
    client.post(f"/drafts/{did}/send")
    row = conn.execute("SELECT status, provider_ref FROM drafts WHERE id = ?", (did,)).fetchone()
    assert row[0] == "exported" and Path(row[1]).exists()
    eml = Path(row[1]).read_text()
    assert "List-Unsubscribe" in eml and "To: info@example-holidays.com.au" in eml
    assert conn.execute("SELECT status FROM accounts WHERE id = ?", (aid,)).fetchone()[0] == "contacted"


def test_gate_blocks_unsourced_and_suppressed(client, tmp_path):
    conn = _db(tmp_path)
    aid, cid = _business(conn, source=None)
    tid = conn.execute("SELECT id FROM templates WHERE name LIKE 'A1%'").fetchone()[0]
    r = client.get(f"/accounts/{aid}/compose?template_id={tid}&contact_id={cid}")
    assert "needs the source URL" in r.get_data(as_text=True)
    conn.execute("UPDATE contacts SET source_url = 'https://example-holidays.com.au/contact'")
    conn.execute("INSERT INTO suppression(value) VALUES ('@example-holidays.com.au')")
    conn.commit()
    r = client.get(f"/accounts/{aid}/compose?template_id={tid}&contact_id={cid}")
    assert "suppression list" in r.get_data(as_text=True)


def test_owner_without_consent_blocked(client, tmp_path):
    conn = _db(tmp_path)
    aid, cid = _business(conn, kind="owner", basis="published_business")
    tid = conn.execute("SELECT id FROM templates WHERE name LIKE 'O1%'").fetchone()[0]
    r = client.get(f"/accounts/{aid}/compose?template_id={tid}&contact_id={cid}")
    assert "Private owners can only be emailed after they opt in" in r.get_data(as_text=True)


def test_capture_creates_consented_owner(client, tmp_path):
    r = client.post("/capture", data={"name": "Sam Owner", "email": "sam@example.com", "address": "1 Test St COOLUM BEACH",
                                      "consent": "1", "code": "CB1", "collection_day": "Tuesday"})
    assert r.status_code == 200
    conn = _db(tmp_path)
    a = conn.execute("SELECT * FROM accounts WHERE kind = 'owner'").fetchone()
    c = conn.execute("SELECT * FROM contacts WHERE account_id = ?", (a["id"],)).fetchone()
    assert c["basis"] == "consent" and c["consent_at"]
    p = conn.execute("SELECT * FROM properties WHERE account_id = ?", (a["id"],)).fetchone()
    assert p["collection_day"] == "Tuesday"
    # owner reply template now passes the gate
    tid = conn.execute("SELECT id FROM templates WHERE name LIKE 'O1%'").fetchone()[0]
    html = client.get(f"/accounts/{a['id']}/compose?template_id={tid}&contact_id={c['id']}").get_data(as_text=True)
    assert "Passes the gate" in html and "Tuesday" in html


def test_capture_requires_consent(client, tmp_path):
    client.post("/capture", data={"name": "X", "email": "x@example.com", "address": "2 Test St"})
    assert _db(tmp_path).execute("SELECT COUNT(*) FROM accounts").fetchone()[0] == 0


def test_letter_flow(client, tmp_path):
    conn = _db(tmp_path)
    conn.execute("INSERT INTO properties(address, suburb, kind, signal, status) VALUES "
                 "('25 Fauna Tce COOLUM BEACH', 'Coolum Beach', 'house', 'short_term_accommodation', 'new')")
    conn.commit()
    r = client.post("/properties/letters", data={"limit": 5})
    assert r.status_code == 302
    d = conn.execute("SELECT * FROM drafts WHERE channel = 'letter'").fetchone()
    assert "The Owner" in d["body"] and "25 Fauna Tce" in d["body"]


@pytest.mark.skipif(not PHASE0.exists(), reason="Phase 0 data not generated")
def test_phase0_import_skips_individuals(client, tmp_path):
    client.post("/admin/import")
    conn = _db(tmp_path)
    names = {r[0] for r in conn.execute("SELECT display_name FROM accounts")}
    assert "Welcome Ready" in names
    assert not {"Michelle", "Cathy Lola", "Tanya", "Sean"} & names
    assert conn.execute("SELECT COUNT(*) FROM contacts WHERE basis = 'published_business' AND source_url IS NULL "
                        "AND email IS NOT NULL").fetchone()[0] == 0


def test_call_window():
    from datetime import datetime
    from leadengine.compliance import BRISBANE, call_window
    assert call_window(datetime(2026, 10, 12, 10, tzinfo=BRISBANE))[0]       # Monday 10am
    assert not call_window(datetime(2026, 10, 11, 10, tzinfo=BRISBANE))[0]   # Sunday
    assert not call_window(datetime(2026, 10, 10, 18, tzinfo=BRISBANE))[0]   # Saturday 6pm
