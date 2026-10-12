"""Command line: python -m leadengine.cli <command>

  init                 create the database and starter templates
  import               load Phase 0 data (hosts, researched contacts, council properties)
  enrich-web [--all]   read business websites for published contacts (accounts with a website)
  abr [--all]          ABN Lookup registered names (needs abr_guid in Settings)
  summarize [--all]    build public-knowledge summaries (Claude if configured)
  hooks                write personalised opening lines for researched accounts
  serve [--port N] [--open]  run the dashboard on http://127.0.0.1:5050
"""
import argparse
import time

from . import db, summarize
from .enrich import abr, website
from .importers import phase0


def _accounts(conn, all_: bool, where: str):
    sql = f"SELECT * FROM accounts WHERE kind = 'business' AND {where}"
    if not all_:
        sql += " AND status IN ('researched','ready')"
    return conn.execute(sql + " ORDER BY listings_active DESC").fetchall()


def main() -> None:
    ap = argparse.ArgumentParser(prog="leadengine")
    ap.add_argument("command", choices=["init", "import", "enrich-web", "abr", "summarize", "hooks", "serve"])
    ap.add_argument("--all", action="store_true", help="include every business account, not just researched")
    ap.add_argument("--port", type=int, default=5050)
    ap.add_argument("--open", action="store_true", help="open the dashboard in your browser")
    args = ap.parse_args()

    if args.command == "serve":
        from .app import create_app
        url = f"http://127.0.0.1:{args.port}"
        if args.open:
            import threading
            import webbrowser
            threading.Timer(1.5, lambda: webbrowser.open(url)).start()
        print(f"Lead Engine running at {url}  (close this window to stop it)")
        create_app().run(host="127.0.0.1", port=args.port, debug=False)
        return

    with db.session() as conn:
        db.init(conn)
        s = db.settings(conn)
        if args.command == "init":
            print(f"Database ready at {db.db_path()}")
        elif args.command == "import":
            print("business hosts:", phase0.import_hosts(conn))
            print("researched accounts:", phase0.import_research(conn))
            print("council properties:", phase0.import_das(conn))
        elif args.command == "enrich-web":
            for a in _accounts(conn, args.all, "website IS NOT NULL AND website != ''"):
                try:
                    print(f"{a['display_name']}: {website.enrich_account(conn, a)}")
                except Exception as e:
                    print(f"{a['display_name']}: failed - {e}")
                conn.commit()
        elif args.command == "abr":
            for a in _accounts(conn, args.all, "abn IS NULL"):
                try:
                    print(f"{a['display_name']}: {abr.enrich_account(conn, a, s.get('abr_guid', ''))}")
                except Exception as e:
                    print(f"{a['display_name']}: failed - {e}")
                conn.commit()
                time.sleep(0.5)
        elif args.command == "summarize":
            for a in _accounts(conn, args.all, "1=1"):
                summarize.summarize_account(conn, a, s)
                conn.commit()
                print("summarised", a["display_name"])
        elif args.command == "hooks":
            for a in _accounts(conn, False, "(hook IS NULL OR hook = '')"):
                print(f"{a['display_name']}: {summarize.write_hook(conn, a, s)}")
                conn.commit()


if __name__ == "__main__":
    main()
