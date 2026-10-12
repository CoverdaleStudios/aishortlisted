"""Import the Phase 0 datasets (bin-caddie-phase0/) into the master database.

- hosts_ranked.csv        -> business accounts (Airbnb hosts that are clearly businesses)
- accounts_batch_*.csv    -> researched business identity + published contacts (with source URLs)
- council_da_targets.csv  -> properties approved for short-stay / secondary dwellings (no names)
- hexes_ranked.csv        -> local short-stay density for each property

Private individuals are never imported by name: hosts that look like people are skipped
unless desk research linked them to a business.
"""
import re
from pathlib import Path

import pandas as pd

from .. import db

PHASE0 = Path(__file__).resolve().parents[3] / "bin-caddie-phase0"
INSIDE_AIRBNB = ("Inside Airbnb - Sunshine Coast, 28 Sep 2026 (internal analysis)",
                 "https://insideairbnb.com/get-the-data/")
SCC_DA = ("Sunshine Coast Council development applications (CC BY 3.0 AU)",
          "https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer")
NOOSA = ("Noosa Heads", "Noosaville", "Sunshine Beach", "Tewantin", "Noosa Hinterland", "Peregian")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PREFERRED_ROLE = re.compile(r"operation|holiday|escape|rental|bdm|property manager|team leader", re.I)
SENIOR_ROLE = re.compile(r"general manager|principal|director|owner|founder|manager", re.I)


def _s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).strip()


def angle_for(top_suburbs: str, houses: int, units: int) -> str:
    first = (top_suburbs or "").split(" (")[0]
    if first.startswith(NOOSA):
        return "B"
    return "C" if units > houses else "A"


def _group(business_name: str) -> str | None:
    if re.search("alloggio", business_name, re.I):
        return "Alloggio Group"
    if re.search("utopia", business_name, re.I):
        return "Stay Utopia"
    return None


def _clean_trading(business_name: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*", " ", business_name).strip(" -|")


def _decision_makers(field: str) -> tuple[list[tuple[str, str]], str | None]:
    field = _s(field)
    if not field:
        return [], None
    urls = re.findall(r"https?://\S+", field)
    url = urls[0].rstrip(").,;") if urls else None
    text = re.sub(r"https?://\S+", "", field)
    people = []
    for chunk in text.split(";"):
        parts = [p.strip(" -()") for p in re.split(r"\s+-\s+", chunk.strip()) if p.strip(" -()")]
        if len(parts) >= 2 and parts[0][0].isalpha() and len(parts[0]) < 40:
            people.append((parts[0], re.sub(r"\(.*", "", parts[1]).strip()))
    return people, url


def _pick_person(people: list[tuple[str, str]]) -> tuple[str, str] | None:
    for rx in (PREFERRED_ROLE, SENIOR_ROLE):
        for name, role in people:
            if rx.search(role):
                return name, role
    return people[0] if people else None


def import_hosts(conn, path: Path | None = None, min_listings: int = 5) -> int:
    path = path or PHASE0 / "outputs" / "hosts_ranked.csv"
    hosts = pd.read_csv(path)
    hosts = hosts[(hosts.active_listings_here >= min_listings) & (hosts.looks_like_business == True)]  # noqa: E712
    n = 0
    for r in hosts.itertuples():
        angle = angle_for(r.top_suburbs, r.houses, r.units)
        conn.execute(
            """INSERT INTO accounts(kind, display_name, trading_name, airbnb_host_id, listings_active, houses,
                   units, top_suburbs, angle, source, created_at, updated_at)
               VALUES ('business', ?, ?, ?, ?, ?, ?, ?, ?, 'inside_airbnb', ?, ?)
               ON CONFLICT(airbnb_host_id) DO UPDATE SET listings_active = excluded.listings_active,
                   houses = excluded.houses, units = excluded.units, top_suburbs = excluded.top_suburbs,
                   updated_at = excluded.updated_at""",
            (r.host_name, r.host_name, str(r.host_id), int(r.active_listings_here), int(r.houses),
             int(r.units), r.top_suburbs, angle, db.now(), db.now()),
        )
        acc = conn.execute("SELECT id FROM accounts WHERE airbnb_host_id = ?", (str(r.host_id),)).fetchone()["id"]
        db.add_fact(conn, f"{int(r.active_listings_here)} active Airbnb listings ({int(r.houses)} houses, "
                          f"{int(r.units)} units), mainly {r.top_suburbs}.",
                    account_id=acc, topic="portfolio", source_name=INSIDE_AIRBNB[0], source_url=INSIDE_AIRBNB[1])
        n += 1
    return n


def import_research(conn, folder: Path | None = None) -> int:
    folder = folder or PHASE0 / "data" / "raw"
    files = sorted(folder.glob("accounts_batch_*.csv"))
    if not files:
        return 0
    hosts = pd.read_csv(PHASE0 / "outputs" / "hosts_ranked.csv").set_index("host_name")
    rows = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
    n = 0
    for r in rows.to_dict("records"):
        status = _s(r.get("status")).lower()
        business = _s(r.get("business_name"))
        if not business or re.search(r"individual|unidentified|do not contact", status):
            continue  # never store private individuals by name
        host = _s(r.get("host_name"))
        h = hosts.loc[host] if host in hosts.index else None
        if isinstance(h, pd.DataFrame):
            h = h.iloc[0]
        host_id = str(h["host_id"]) if h is not None else f"research:{host}"
        trading = _clean_trading(business)
        listings = int(h["active_listings_here"]) if h is not None else 0
        houses = int(h["houses"]) if h is not None else 0
        units = int(h["units"]) if h is not None else 0
        top = h["top_suburbs"] if h is not None else ""
        conn.execute(
            """INSERT INTO accounts(kind, display_name, trading_name, airbnb_host_id, listings_active, houses, units,
                   top_suburbs, angle, website, business_type, office_suburb, group_name, no_marketing_notice,
                   status, source, created_at, updated_at)
               VALUES ('business', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'researched', 'desk_research', ?, ?)
               ON CONFLICT(airbnb_host_id) DO UPDATE SET display_name = excluded.display_name,
                   trading_name = excluded.trading_name, website = excluded.website,
                   business_type = excluded.business_type, office_suburb = excluded.office_suburb,
                   group_name = excluded.group_name, no_marketing_notice = excluded.no_marketing_notice,
                   status = CASE WHEN accounts.status = 'new' THEN 'researched' ELSE accounts.status END,
                   updated_at = excluded.updated_at""",
            (trading, trading, host_id, listings, houses, units, top, angle_for(top, houses, units),
             _s(r.get("website")), _s(r.get("business_type")), _s(r.get("office_suburb")), _group(business),
             (_s(r.get("no_marketing_notice")) or "unknown").lower(), db.now(), db.now()),
        )
        acc = conn.execute("SELECT id FROM accounts WHERE airbnb_host_id = ?", (host_id,)).fetchone()["id"]

        people, dm_url = _decision_makers(r.get("decision_maker"))
        person = _pick_person(people)
        emails = EMAIL_RE.findall(_s(r.get("published_email")))
        email_ok = emails and not re.search(r"sister-brand|guest-facing|partner form", status)
        phone = re.split(r"\s*[/;]\s*|\s\(", _s(r.get("published_phone")))[0].strip() or None
        db.upsert_contact(
            conn, acc, email=emails[0] if email_ok else None, phone=phone,
            name=person[0] if person else None, role=person[1] if person else None,
            basis="published_business",
            source_url=_s(r.get("email_source_url")) if email_ok else _s(r.get("phone_source_url")) or None,
            is_primary=1,
        )
        for name, role in people:
            db.add_fact(conn, f"{name} - {role} (named on the business's own site).", account_id=acc,
                        topic="people", source_name="Business website", source_url=dm_url)
        site = _s(r.get("website")) or None
        for col, topic in (("portfolio_notes", "portfolio"), ("current_bin_or_cleaning_mentions", "services"),
                           ("pitch_angle", "research")):
            if _s(r.get(col)):
                db.add_fact(conn, _s(r.get(col)), account_id=acc, topic=topic,
                            source_name="Desk research (Phase 0)", source_url=site)
        n += 1
    return n


def import_das(conn, path: Path | None = None, hex_path: Path | None = None) -> int:
    path = path or PHASE0 / "outputs" / "council_da_targets.csv"
    hex_path = hex_path or PHASE0 / "outputs" / "hexes_ranked.csv"
    das = pd.read_csv(path)
    hexes = pd.read_csv(hex_path).set_index("hex") if hex_path.exists() else pd.DataFrame()
    n = 0
    for r in das.itertuples():
        address = _s(r.address)
        if not address:
            continue
        m = re.search(r"((?:[A-Z]{2,}\s?)+)$", address)
        suburb = m.group(1).strip().title() if m else ""
        hx = hexes.loc[r.hex] if (not hexes.empty and isinstance(r.hex, str) and r.hex in hexes.index) else None
        kind = "complex" if r.pitch.startswith("body") else "house"
        conn.execute(
            """INSERT INTO properties(address, suburb, lat, lng, hex, kind, signal, da_ram_id, da_use, da_date,
                   da_status, hex_active_listings, hex_self_managed_houses, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(address, signal) DO UPDATE SET da_status = excluded.da_status,
                   hex_active_listings = excluded.hex_active_listings, updated_at = excluded.updated_at""",
            (address, suburb, r.lat, r.lng, _s(r.hex), kind, r.signal, _s(r.ram_id), _s(r.use),
             _s(r.date_received)[:10], _s(r.status),
             int(hx["active_listings"]) if hx is not None else 0,
             int(hx["self_managed_houses"]) if hx is not None else 0, db.now(), db.now()),
        )
        pid = conn.execute("SELECT id FROM properties WHERE address = ? AND signal = ?",
                           (address, r.signal)).fetchone()["id"]
        db.add_fact(conn, f"Council application {_s(r.ram_id)}: {_s(r.use) or r.signal.replace('_', ' ')} "
                          f"(received {_s(r.date_received)[:10]}, {_s(r.status).lower()}).",
                    property_id=pid, topic="planning", source_name=SCC_DA[0], source_url=SCC_DA[1])
        if hx is not None:
            db.add_fact(conn, f"About {int(hx['active_listings'])} active short-stay listings within ~500 m "
                              f"({int(hx['self_managed_houses'])} self-managed houses).",
                        property_id=pid, topic="market", source_name=INSIDE_AIRBNB[0], source_url=INSIDE_AIRBNB[1])
        n += 1
    return n
