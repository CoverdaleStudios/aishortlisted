"""Bin Caddie Lead Engine - local web dashboard.

Run:  python -m leadengine.cli serve   (then open http://127.0.0.1:5050)
"""
import csv
import io
import json
from datetime import datetime, timezone

from flask import Flask, Response, abort, flash, g, redirect, render_template, request, url_for

from . import compliance, db, summarize, templating
from .enrich import abr, website
from .importers import phase0
from .mail import providers

CONSENT_TEXT = ("I agree to Bin Caddie Property Services contacting me by email or phone about its bin "
                "services for this property. I can unsubscribe at any time.")


def create_app(db_path=None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "local-only"  # dashboard is meant to run on localhost
    app.config["DB_PATH"] = db_path

    with db.session(db_path) as conn:
        db.init(conn)

    def conn():
        if "conn" not in g:
            g.conn = db.connect(app.config["DB_PATH"])
        return g.conn

    @app.teardown_appcontext
    def _close(_exc):
        c = g.pop("conn", None)
        if c is not None:
            c.commit()
            c.close()

    @app.context_processor
    def _globals():
        return {"statuses": db.ACCOUNT_STATUSES, "now": datetime.now(timezone.utc)}

    def S():
        return db.settings(conn())

    def account_or_404(aid):
        a = conn().execute("SELECT * FROM accounts WHERE id = ?", (aid,)).fetchone()
        return a or abort(404)

    def sent_today() -> int:
        today = datetime.now(timezone.utc).date().isoformat()
        return conn().execute("SELECT COUNT(*) FROM drafts WHERE status IN ('sent','exported') "
                              "AND substr(sent_at, 1, 10) = ?", (today,)).fetchone()[0]

    def make_draft(account, contact, tmpl, prop=None):
        s = S()
        ctx = templating.context_for(s, account, contact, prop)
        subject, body, problems = templating.render(tmpl, ctx, s)
        if tmpl["channel"] == "email":
            report = compliance.check_email(conn(), s, account, contact, body, sent_today())
        else:
            report = compliance.check_letter(conn(), prop)
        report["warnings"] = problems + report["warnings"]
        cur = conn().execute(
            """INSERT INTO drafts(account_id, contact_id, property_id, template_id, channel, to_address, subject,
                   body, status, compliance, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?)""",
            (account["id"] if account else None, contact["id"] if contact else None, prop["id"] if prop else None,
             tmpl["id"], tmpl["channel"], (contact["email"] if contact else None) or (prop["address"] if prop else None),
             subject, body, db.as_json(report), db.now()),
        )
        return cur.lastrowid, report

    # ------------------------------------------------------------------ dashboard
    @app.route("/")
    def dashboard():
        c = conn()
        stats = {
            "accounts": c.execute("SELECT COUNT(*) FROM accounts WHERE kind='business'").fetchone()[0],
            "owners": c.execute("SELECT COUNT(*) FROM accounts WHERE kind='owner'").fetchone()[0],
            "properties": c.execute("SELECT COUNT(*) FROM properties").fetchone()[0],
            "contacts_email": c.execute("SELECT COUNT(DISTINCT account_id) FROM contacts WHERE email IS NOT NULL").fetchone()[0],
            "drafts": c.execute("SELECT COUNT(*) FROM drafts WHERE status='draft'").fetchone()[0],
            "approved": c.execute("SELECT COUNT(*) FROM drafts WHERE status='approved'").fetchone()[0],
            "sent": c.execute("SELECT COUNT(*) FROM drafts WHERE status IN ('sent','exported')").fetchone()[0],
            "suppressed": c.execute("SELECT COUNT(*) FROM suppression").fetchone()[0],
        }
        by_status = c.execute("SELECT status, COUNT(*) n, SUM(listings_active) l FROM accounts "
                              "GROUP BY status ORDER BY n DESC").fetchall()
        top = c.execute("SELECT * FROM accounts WHERE kind='business' AND status NOT IN ('do_not_contact','not_interested') "
                        "ORDER BY listings_active DESC LIMIT 10").fetchall()
        ok, msg = compliance.call_window()
        return render_template("dashboard.html", stats=stats, by_status=by_status, top=top,
                               call_ok=ok, call_msg=msg, settings=S())

    @app.post("/admin/import")
    def run_import():
        c = conn()
        try:
            n1 = phase0.import_hosts(c)
            n2 = phase0.import_research(c)
            n3 = phase0.import_das(c)
            flash(f"Imported {n1} business hosts, {n2} researched accounts, {n3} council properties.")
        except FileNotFoundError as e:
            flash(f"Phase 0 data not found ({e.filename}). Run the bin-caddie-phase0 scripts first.", "error")
        return redirect(url_for("dashboard"))

    # ------------------------------------------------------------------ accounts
    @app.route("/accounts")
    def accounts():
        q, status, angle, kind = (request.args.get(k, "") for k in ("q", "status", "angle", "kind"))
        sql = ("SELECT a.*, (SELECT email FROM contacts WHERE account_id=a.id AND email IS NOT NULL "
               "ORDER BY is_primary DESC LIMIT 1) AS email FROM accounts a WHERE 1=1")
        args = []
        if q:
            sql += " AND (display_name LIKE ? OR trading_name LIKE ? OR registered_name LIKE ? OR top_suburbs LIKE ?)"
            args += [f"%{q}%"] * 4
        for col, val in (("status", status), ("angle", angle), ("kind", kind)):
            if val:
                sql += f" AND a.{col} = ?"
                args.append(val)
        rows = conn().execute(sql + " ORDER BY listings_active DESC, display_name LIMIT 500", args).fetchall()
        return render_template("accounts.html", rows=rows, q=q, status=status, angle=angle, kind=kind)

    @app.route("/accounts/<int:aid>")
    def account(aid):
        c = conn()
        a = account_or_404(aid)
        contacts = c.execute("SELECT * FROM contacts WHERE account_id = ? ORDER BY is_primary DESC, id", (aid,)).fetchall()
        facts = summarize.facts_for(c, account_id=aid)
        summary = c.execute("SELECT * FROM summaries WHERE account_id = ? ORDER BY id DESC LIMIT 1", (aid,)).fetchone()
        touches = c.execute("SELECT * FROM touches WHERE account_id = ? ORDER BY happened_at DESC", (aid,)).fetchall()
        drafts = c.execute("SELECT * FROM drafts WHERE account_id = ? ORDER BY id DESC", (aid,)).fetchall()
        props = c.execute("SELECT * FROM properties WHERE account_id = ?", (aid,)).fetchall()
        group = (c.execute("SELECT id, display_name, listings_active FROM accounts WHERE group_name = ? AND id != ?",
                           (a["group_name"], aid)).fetchall() if a["group_name"] else [])
        audience = "owner" if a["kind"] == "owner" else "business"
        tmpls = c.execute("SELECT * FROM templates WHERE active = 1 AND audience = ? ORDER BY name", (audience,)).fetchall()
        return render_template("account.html", a=a, contacts=contacts, facts=facts, summary=summary,
                               touches=touches, drafts=drafts, props=props, group=group, templates=tmpls,
                               plain=summarize.plain_summary(a, facts), llm=summarize.llm_available(S()))

    @app.post("/accounts/<int:aid>/update")
    def account_update(aid):
        account_or_404(aid)
        fields = ["status", "angle", "hook", "notes", "website", "trading_name", "group_name", "no_marketing_notice"]
        vals = {f: request.form.get(f) for f in fields if f in request.form}
        if vals:
            sets = ", ".join(f"{k} = ?" for k in vals)
            conn().execute(f"UPDATE accounts SET {sets}, updated_at = ? WHERE id = ?", [*vals.values(), db.now(), aid])
        flash("Saved.")
        return redirect(url_for("account", aid=aid))

    @app.post("/accounts/<int:aid>/contacts")
    def contact_add(aid):
        a = account_or_404(aid)
        f = request.form
        basis = f.get("basis", "published_business")
        if basis == "published_business" and not f.get("source_url"):
            flash("A published business contact needs the URL where it is published.", "error")
            return redirect(url_for("account", aid=aid))
        if a["kind"] == "owner" and basis == "published_business":
            flash("Owners can only be added with consent or referral basis.", "error")
            return redirect(url_for("account", aid=aid))
        db.upsert_contact(conn(), aid, email=(f.get("email") or None), phone=(f.get("phone") or None),
                          name=(f.get("name") or None), role=(f.get("role") or None), basis=basis,
                          source_url=(f.get("source_url") or None), consent_text=(f.get("consent_text") or None),
                          is_primary=1 if f.get("is_primary") else 0)
        flash("Contact added.")
        return redirect(url_for("account", aid=aid))

    @app.post("/contacts/<int:cid>/delete")
    def contact_delete(cid):
        row = conn().execute("SELECT account_id FROM contacts WHERE id = ?", (cid,)).fetchone() or abort(404)
        conn().execute("DELETE FROM contacts WHERE id = ?", (cid,))
        return redirect(url_for("account", aid=row["account_id"]))

    @app.post("/accounts/<int:aid>/enrich/<kind>")
    def account_enrich(aid, kind):
        a = account_or_404(aid)
        try:
            if kind == "web":
                msg = website.enrich_account(conn(), a)
            elif kind == "abr":
                msg = abr.enrich_account(conn(), a, S().get("abr_guid", ""))
            elif kind == "summary":
                summarize.summarize_account(conn(), a, S())
                msg = "Summary updated."
            elif kind == "hook":
                msg = "Hook: " + (summarize.write_hook(conn(), a, S()) or "(none)")
            else:
                abort(404)
            flash(msg)
        except Exception as e:  # surface enrichment failures in the UI rather than a 500
            flash(f"{kind} failed: {e}", "error")
        return redirect(url_for("account", aid=aid))

    @app.post("/accounts/<int:aid>/touch")
    def account_touch(aid):
        account_or_404(aid)
        f = request.form
        conn().execute("INSERT INTO touches(account_id, happened_at, channel, outcome, notes) VALUES (?, ?, ?, ?, ?)",
                       (aid, f.get("happened_at") or db.now()[:10], f.get("channel"), f.get("outcome"), f.get("notes")))
        status_for = {"meeting booked": "meeting", "pilot agreed": "pilot", "replied": "replied",
                      "not interested": "not_interested", "unsubscribe": "do_not_contact"}
        if f.get("outcome") in status_for:
            conn().execute("UPDATE accounts SET status = ?, updated_at = ? WHERE id = ?",
                           (status_for[f["outcome"]], db.now(), aid))
        if f.get("outcome") == "unsubscribe":
            for ct in conn().execute("SELECT email, phone FROM contacts WHERE account_id = ?", (aid,)):
                for v in (ct["email"], ct["phone"]):
                    if v:
                        conn().execute("INSERT OR IGNORE INTO suppression(value, reason, created_at) VALUES (?, ?, ?)",
                                       (v.lower(), "unsubscribed", db.now()))
        flash("Logged.")
        return redirect(url_for("account", aid=aid))

    @app.route("/accounts/<int:aid>/compose", methods=["GET", "POST"])
    def compose(aid):
        a = account_or_404(aid)
        c = conn()
        tid = request.values.get("template_id", type=int)
        cid = request.values.get("contact_id", type=int)
        tmpl = c.execute("SELECT * FROM templates WHERE id = ?", (tid,)).fetchone() or abort(400)
        contact = c.execute("SELECT * FROM contacts WHERE id = ? AND account_id = ?", (cid, aid)).fetchone() if cid else None
        prop = c.execute("SELECT * FROM properties WHERE account_id = ? LIMIT 1", (aid,)).fetchone()
        if request.method == "POST":
            did, report = make_draft(a, contact, tmpl, prop)
            flash("Draft saved." + (" Fix the compliance errors before approving." if report["errors"] else ""))
            return redirect(url_for("draft", did=did))
        s = S()
        subject, body, problems = templating.render(tmpl, templating.context_for(s, a, contact, prop), s)
        report = (compliance.check_email(c, s, a, contact, body, sent_today()) if tmpl["channel"] == "email"
                  else {"errors": [], "warnings": []})
        return render_template("compose.html", a=a, tmpl=tmpl, contact=contact, subject=subject, body=body,
                               report=report, problems=problems)

    @app.route("/bulk", methods=["GET", "POST"])
    def bulk():
        """Create personalised drafts for every eligible account matching a filter."""
        c = conn()
        tmpls = c.execute("SELECT * FROM templates WHERE active = 1 AND audience = 'business' ORDER BY name").fetchall()
        if request.method == "GET":
            return render_template("bulk.html", templates=tmpls)
        f = request.form
        by_angle = f.get("template_mode") == "by_angle"
        sql = "SELECT * FROM accounts WHERE kind = 'business' AND status IN ('researched','ready')"
        args = []
        if f.get("angle"):
            sql += " AND angle = ?"
            args.append(f["angle"])
        if f.get("min_listings"):
            sql += " AND listings_active >= ?"
            args.append(int(f["min_listings"]))
        made, skipped, seen_groups = 0, [], set()
        for a in c.execute(sql + " ORDER BY listings_active DESC LIMIT ?", [*args, int(f.get("limit") or 15)]).fetchall():
            if a["group_name"]:
                if a["group_name"] in seen_groups:
                    skipped.append(f"{a['display_name']}: same group as an earlier account")
                    continue
                seen_groups.add(a["group_name"])
            if c.execute("SELECT 1 FROM drafts WHERE account_id = ? AND status IN ('draft','approved')", (a["id"],)).fetchone():
                skipped.append(f"{a['display_name']}: already has a pending draft")
                continue
            contact = c.execute("SELECT * FROM contacts WHERE account_id = ? AND email IS NOT NULL "
                                "ORDER BY is_primary DESC LIMIT 1", (a["id"],)).fetchone()
            if not contact:
                skipped.append(f"{a['display_name']}: no published email (phone task instead)")
                continue
            if by_angle:
                tmpl = c.execute("SELECT * FROM templates WHERE active = 1 AND audience='business' AND angle = ? "
                                 "ORDER BY name LIMIT 1", (a["angle"] or "A",)).fetchone()
            else:
                tmpl = c.execute("SELECT * FROM templates WHERE id = ?", (f.get("template_id", type=int),)).fetchone()
            if not tmpl:
                skipped.append(f"{a['display_name']}: no template")
                continue
            make_draft(a, contact, tmpl)
            made += 1
        return render_template("bulk.html", templates=tmpls, made=made, skipped=skipped)

    # ------------------------------------------------------------------ properties
    @app.route("/properties")
    def properties():
        signal, status, q = (request.args.get(k, "") for k in ("signal", "status", "q"))
        sql, args = "SELECT * FROM properties WHERE 1=1", []
        if signal:
            sql += " AND signal = ?"
            args.append(signal)
        if status:
            sql += " AND status = ?"
            args.append(status)
        if q:
            sql += " AND (address LIKE ? OR suburb LIKE ?)"
            args += [f"%{q}%"] * 2
        rows = conn().execute(sql + " ORDER BY (signal='short_term_accommodation') DESC, da_date DESC LIMIT 500",
                              args).fetchall()
        return render_template("properties.html", rows=rows, signal=signal, status=status, q=q)

    @app.route("/properties/<int:pid>")
    def property_detail(pid):
        c = conn()
        p = c.execute("SELECT * FROM properties WHERE id = ?", (pid,)).fetchone() or abort(404)
        facts = summarize.facts_for(c, property_id=pid)
        owner = c.execute("SELECT * FROM accounts WHERE id = ?", (p["account_id"],)).fetchone() if p["account_id"] else None
        drafts = c.execute("SELECT * FROM drafts WHERE property_id = ? ORDER BY id DESC", (pid,)).fetchall()
        return render_template("property.html", p=p, facts=facts, owner=owner, drafts=drafts,
                               summary=summarize.property_summary(p, facts))

    @app.post("/properties/<int:pid>/letter")
    def property_letter(pid):
        c = conn()
        p = c.execute("SELECT * FROM properties WHERE id = ?", (pid,)).fetchone() or abort(404)
        tmpl = c.execute("SELECT * FROM templates WHERE channel = 'letter' AND active = 1 ORDER BY id LIMIT 1").fetchone()
        did, _ = make_draft(None, None, tmpl, p)
        c.execute("UPDATE properties SET status = 'letter_queued', updated_at = ? WHERE id = ?", (db.now(), pid))
        return redirect(url_for("draft", did=did))

    @app.post("/properties/letters")
    def property_letters_bulk():
        c = conn()
        n = int(request.form.get("limit") or 50)
        tmpl = c.execute("SELECT * FROM templates WHERE channel = 'letter' AND active = 1 ORDER BY id LIMIT 1").fetchone()
        rows = c.execute("SELECT * FROM properties WHERE status = 'new' AND signal = 'short_term_accommodation' "
                         "AND kind = 'house' ORDER BY da_date DESC LIMIT ?", (n,)).fetchall()
        for p in rows:
            make_draft(None, None, tmpl, p)
            c.execute("UPDATE properties SET status = 'letter_queued', updated_at = ? WHERE id = ?", (db.now(), p["id"]))
        flash(f"Queued {len(rows)} 'To the Owner' letters - print them from the Outbox.")
        return redirect(url_for("outbox", channel="letter"))

    # ------------------------------------------------------------------ outbox
    @app.route("/outbox")
    def outbox():
        status = request.args.get("status", "")
        channel = request.args.get("channel", "")
        sql = ("SELECT d.*, a.display_name, p.address FROM drafts d LEFT JOIN accounts a ON a.id = d.account_id "
               "LEFT JOIN properties p ON p.id = d.property_id WHERE 1=1")
        args = []
        if status:
            sql += " AND d.status = ?"
            args.append(status)
        if channel:
            sql += " AND d.channel = ?"
            args.append(channel)
        rows = conn().execute(sql + " ORDER BY d.id DESC LIMIT 500", args).fetchall()
        return render_template("outbox.html", rows=rows, status=status, channel=channel,
                               provider=S().get("email_provider"), sent_today=sent_today(),
                               cap=S().get("daily_send_cap"), json=json)

    @app.route("/drafts/<int:did>", methods=["GET", "POST"])
    def draft(did):
        c = conn()
        d = c.execute("SELECT * FROM drafts WHERE id = ?", (did,)).fetchone() or abort(404)
        if request.method == "POST" and d["status"] == "draft":
            c.execute("UPDATE drafts SET subject = ?, body = ? WHERE id = ?",
                      (request.form.get("subject"), request.form.get("body"), did))
            flash("Edits saved. Approve to re-run the compliance check.")
            return redirect(url_for("draft", did=did))
        a = c.execute("SELECT * FROM accounts WHERE id = ?", (d["account_id"],)).fetchone() if d["account_id"] else None
        p = c.execute("SELECT * FROM properties WHERE id = ?", (d["property_id"],)).fetchone() if d["property_id"] else None
        report = json.loads(d["compliance"] or '{"errors":[],"warnings":[]}')
        if request.args.get("print"):
            return render_template("letter_print.html", d=d, p=p)
        return render_template("draft.html", d=d, a=a, p=p, report=report)

    def approve_draft(did) -> dict:
        c = conn()
        d = c.execute("SELECT * FROM drafts WHERE id = ?", (did,)).fetchone() or abort(404)
        if d["channel"] == "email":
            a = c.execute("SELECT * FROM accounts WHERE id = ?", (d["account_id"],)).fetchone()
            ct = c.execute("SELECT * FROM contacts WHERE id = ?", (d["contact_id"],)).fetchone()
            report = compliance.check_email(c, S(), a, ct, d["body"], sent_today())
        else:
            p = c.execute("SELECT * FROM properties WHERE id = ?", (d["property_id"],)).fetchone()
            report = compliance.check_letter(c, p)
        if report["errors"]:
            c.execute("UPDATE drafts SET compliance = ? WHERE id = ?", (db.as_json(report), did))
        else:
            c.execute("UPDATE drafts SET status = 'approved', approved_at = ?, compliance = ? WHERE id = ?",
                      (db.now(), db.as_json(report), did))
        return report

    @app.post("/drafts/<int:did>/approve")
    def draft_approve(did):
        report = approve_draft(did)
        if report["errors"]:
            flash("Not approved - fix the compliance errors first.", "error")
        else:
            flash("Approved.")
        return redirect(url_for("draft", did=did))

    def deliver(d) -> str:
        c = conn()
        s = S()
        if d["channel"] == "letter":
            c.execute("UPDATE drafts SET status = 'sent', sent_at = ?, provider = 'print' WHERE id = ?", (db.now(), d["id"]))
            c.execute("UPDATE properties SET status = 'letter_sent', updated_at = ? WHERE id = ?", (db.now(), d["property_id"]))
            c.execute("INSERT INTO touches(property_id, happened_at, channel, outcome) VALUES (?, ?, 'mail', 'letter sent')",
                      (d["property_id"], db.now()[:10]))
            return "marked as posted"
        a = c.execute("SELECT * FROM accounts WHERE id = ?", (d["account_id"],)).fetchone()
        ct = c.execute("SELECT * FROM contacts WHERE id = ?", (d["contact_id"],)).fetchone()
        report = compliance.check_email(c, s, a, ct, d["body"], sent_today())
        if report["errors"]:
            raise RuntimeError("; ".join(report["errors"]))
        provider = providers.get_provider(s)
        ref = provider.send(providers.build_message(s, ct["email"], d["subject"], d["body"]))
        status = "exported" if provider.name == "outbox" else "sent"
        c.execute("UPDATE drafts SET status = ?, sent_at = ?, provider = ?, provider_ref = ? WHERE id = ?",
                  (status, db.now(), provider.name, ref, d["id"]))
        c.execute("INSERT INTO touches(account_id, happened_at, channel, outcome, notes) VALUES (?, ?, 'email', 'no reply', ?)",
                  (a["id"], db.now()[:10], f"{status}: {d['subject']}"))
        if a["status"] in ("new", "researched", "ready"):
            c.execute("UPDATE accounts SET status = 'contacted', updated_at = ? WHERE id = ?", (db.now(), a["id"]))
        return f"{status} via {provider.name}"

    @app.post("/drafts/<int:did>/send")
    def draft_send(did):
        d = conn().execute("SELECT * FROM drafts WHERE id = ?", (did,)).fetchone() or abort(404)
        if d["status"] != "approved":
            flash("Approve the draft first.", "error")
        else:
            try:
                flash("Done: " + deliver(d))
            except Exception as e:
                conn().execute("UPDATE drafts SET status = 'failed', error = ? WHERE id = ?", (str(e), did))
                flash(f"Send failed: {e}", "error")
        return redirect(url_for("draft", did=did))

    @app.post("/drafts/<int:did>/cancel")
    def draft_cancel(did):
        conn().execute("UPDATE drafts SET status = 'cancelled' WHERE id = ?", (did,))
        return redirect(url_for("outbox"))

    @app.post("/outbox/approve-all")
    def approve_all():
        ok = bad = 0
        for d in conn().execute("SELECT id FROM drafts WHERE status = 'draft'").fetchall():
            if approve_draft(d["id"])["errors"]:
                bad += 1
            else:
                ok += 1
        flash(f"Approved {ok}; {bad} need fixes.")
        return redirect(url_for("outbox"))

    @app.post("/outbox/send-approved")
    def send_approved():
        done, failed = 0, []
        for d in conn().execute("SELECT * FROM drafts WHERE status = 'approved' AND channel = 'email' ORDER BY id").fetchall():
            try:
                deliver(d)
                done += 1
            except Exception as e:
                failed.append(f"#{d['id']}: {e}")
                conn().execute("UPDATE drafts SET status = 'failed', error = ? WHERE id = ?", (str(e), d["id"]))
        flash(f"Delivered {done}." + (" Failed: " + " | ".join(failed[:5]) if failed else ""))
        return redirect(url_for("outbox"))

    # ------------------------------------------------------------------ templates
    @app.route("/templates")
    def templates_list():
        return render_template("templates.html", rows=conn().execute("SELECT * FROM templates ORDER BY audience, name").fetchall())

    @app.route("/templates/<int:tid>", methods=["GET", "POST"])
    def template_edit(tid):
        c = conn()
        if request.method == "POST":
            f = request.form
            if tid == 0:
                c.execute("INSERT INTO templates(name, audience, angle, channel, subject, body, active, updated_at) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (f["name"], f["audience"], f.get("angle"), f["channel"], f.get("subject"), f["body"],
                           1 if f.get("active") else 0, db.now()))
            else:
                c.execute("UPDATE templates SET name=?, audience=?, angle=?, channel=?, subject=?, body=?, active=?, "
                          "updated_at=? WHERE id=?", (f["name"], f["audience"], f.get("angle"), f["channel"],
                                                     f.get("subject"), f["body"], 1 if f.get("active") else 0, db.now(), tid))
            flash("Template saved.")
            return redirect(url_for("templates_list"))
        t = c.execute("SELECT * FROM templates WHERE id = ?", (tid,)).fetchone() if tid else None
        sample = c.execute("SELECT * FROM accounts WHERE kind='business' ORDER BY listings_active DESC LIMIT 1").fetchone()
        preview = None
        if t and sample:
            ct = c.execute("SELECT * FROM contacts WHERE account_id = ? ORDER BY is_primary DESC LIMIT 1", (sample["id"],)).fetchone()
            p = c.execute("SELECT * FROM properties ORDER BY id LIMIT 1").fetchone() if t["channel"] == "letter" else None
            s = S()
            preview = templating.render(t, templating.context_for(s, sample, ct, p), s)
        return render_template("template_edit.html", t=t, preview=preview, sample=sample)

    # ------------------------------------------------------------------ suppression / settings
    @app.route("/suppression", methods=["GET", "POST"])
    def suppression():
        if request.method == "POST":
            v = (request.form.get("value") or "").strip().lower()
            if v:
                conn().execute("INSERT OR IGNORE INTO suppression(value, reason, created_at) VALUES (?, ?, ?)",
                               (v, request.form.get("reason") or "opt-out", db.now()))
                flash(f"Suppressed {v}.")
            return redirect(url_for("suppression"))
        return render_template("suppression.html", rows=conn().execute("SELECT * FROM suppression ORDER BY id DESC").fetchall())

    @app.route("/settings", methods=["GET", "POST"])
    def settings_page():
        if request.method == "POST":
            for k in db.DEFAULT_SETTINGS:
                if k in request.form:
                    db.set_setting(conn(), k, request.form[k].strip())
            flash("Settings saved.")
            return redirect(url_for("settings_page"))
        return render_template("settings.html", s=S(), llm=summarize.llm_available(S()))

    # ------------------------------------------------------------------ owner opt-in capture
    @app.route("/capture", methods=["GET", "POST"])
    def capture():
        """Public-facing form (QR codes on flyers/letters point here). The only way private owners
        enter the system with their name and email - with recorded consent."""
        if request.method == "GET":
            return render_template("capture.html", consent=CONSENT_TEXT, code=request.args.get("code", ""))
        f = request.form
        if not f.get("consent"):
            flash("Please tick the consent box so we can contact you.", "error")
            return render_template("capture.html", consent=CONSENT_TEXT, code=f.get("code", ""), form=f)
        c = conn()
        name = f.get("name", "").strip()
        cur = c.execute("INSERT INTO accounts(kind, display_name, status, source, notes, created_at, updated_at) "
                        "VALUES ('owner', ?, 'replied', ?, ?, ?, ?)",
                        (name or f.get("email"), f"capture:{f.get('code') or 'direct'}", f.get("message"), db.now(), db.now()))
        aid = cur.lastrowid
        db.upsert_contact(c, aid, email=f.get("email") or None, phone=f.get("phone") or None, name=name or None,
                          basis="consent", consent_text=CONSENT_TEXT, is_primary=1)
        address = f.get("address", "").strip()
        if address:
            existing = c.execute("SELECT id FROM properties WHERE lower(address) = lower(?)", (address,)).fetchone()
            if existing:
                c.execute("UPDATE properties SET account_id = ?, status = 'responded', collection_day = ?, updated_at = ? "
                          "WHERE id = ?", (aid, f.get("collection_day"), db.now(), existing["id"]))
            else:
                c.execute("INSERT INTO properties(account_id, address, kind, signal, collection_day, status, created_at, "
                          "updated_at) VALUES (?, ?, ?, 'owner_provided', ?, 'responded', ?, ?)",
                          (aid, address, f.get("kind") or "house", f.get("collection_day"), db.now(), db.now()))
        db.add_fact(c, f"Enquiry via {f.get('code') or 'website form'}: {f.get('bins') or '?'} bins, "
                       f"{f.get('kind') or 'house'}, collection day {f.get('collection_day') or 'unknown'}.",
                    account_id=aid, topic="enquiry", source_name="Owner (consented form)")
        return render_template("capture_thanks.html")

    # ------------------------------------------------------------------ export
    @app.route("/export/accounts.csv")
    def export_accounts():
        rows = conn().execute(
            "SELECT a.id, a.kind, a.display_name, a.trading_name, a.registered_name, a.abn, a.status, a.angle, "
            "a.listings_active, a.houses, a.units, a.top_suburbs, a.group_name, c.name AS contact_name, c.role, "
            "c.email, c.phone, c.basis, c.source_url FROM accounts a LEFT JOIN contacts c "
            "ON c.account_id = a.id AND c.is_primary = 1 ORDER BY a.listings_active DESC").fetchall()
        buf = io.StringIO()
        w = csv.writer(buf)
        if rows:
            w.writerow(rows[0].keys())
            w.writerows([tuple(r) for r in rows])
        return Response(buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment; filename=accounts.csv"})

    return app
