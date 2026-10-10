"""Step 2: pull Sunshine Coast Council development applications that signal short-stay use.

Source : Sunshine Coast Council open data (CC BY 3.0 AU)
         https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer
Output : outputs/council_da_targets.csv

Privacy: the council description often ends with owner/applicant names. This script
keeps ONLY the street address and the described use, and drops every name. Letters go
to "The Owner" at the address - never to a named person.
"""
import re
import time
from pathlib import Path

import h3
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

BASE = "https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer"
LAYERS = {0: "In progress", 1: "Decided or past"}
H3_RES = 8

QUERIES = {
    "short_term_accommodation": "(UPPER(description) LIKE '%SHORT-TERM ACCOMMODATION%' "
                                "OR UPPER(description) LIKE '%SHORT TERM ACCOMMODATION%')",
    "dual_occupancy": "UPPER(description) LIKE '%DUAL OCCUPANCY%' AND d_date_rec >= DATE '2023-01-01'",
    "secondary_dwelling": "UPPER(description) LIKE '%SECONDARY DWELLING%' AND d_date_rec >= DATE '2023-01-01'",
}
BAD_DECISIONS = re.compile(r"WITHDRAWN|REFUS|LAPSED|NOT PROPERLY|CANCEL", re.I)
COMPLEX_HINT = re.compile(r"\(([2-9]|\d{2,})\s*units?\)|\bunits\b|multiple dwelling|resort|apartments|villas|hotel", re.I)


def fetch(layer: int, where: str) -> list[dict]:
    rows, offset = [], 0
    while True:
        r = requests.get(f"{BASE}/{layer}/query", params={
            "where": where, "outFields": "*", "returnGeometry": "true", "outSR": 4326,
            "resultOffset": offset, "resultRecordCount": 1000, "f": "json",
        }, timeout=60)
        r.raise_for_status()
        d = r.json()
        if "error" in d:
            raise RuntimeError(d["error"])
        feats = d.get("features", [])
        rows += feats
        if not d.get("exceededTransferLimit") or not feats:
            return rows
        offset += len(feats)
        time.sleep(0.5)


def centroid(geom: dict | None) -> tuple[float | None, float | None]:
    if not geom or "rings" not in geom:
        return None, None
    pts = [p for ring in geom["rings"] for p in ring]
    return sum(p[1] for p in pts) / len(pts), sum(p[0] for p in pts) / len(pts)


def split_description(desc: str) -> tuple[str, str]:
    """'59 Ayrshire Rd YANDINA - Short-Term Accommodation - J Smith' -> (address, use)."""
    desc = re.sub(r"^#+\s*\w+\s*#+\s*", "", desc or "").strip()
    parts = [p.strip() for p in re.split(r"\s+[-–]\s+", desc) if p.strip()]
    address = parts[0] if parts else ""
    use = parts[1] if len(parts) > 1 else ""
    return address, use  # parts[2:] are names -> deliberately discarded


def main() -> None:
    records = []
    for signal, where in QUERIES.items():
        for layer, status in LAYERS.items():
            feats = fetch(layer, where)
            print(f"{signal:26s} {status:16s} {len(feats):5d}")
            for f in feats:
                a = f["attributes"]
                address, use = split_description(a.get("description", ""))
                lat, lng = centroid(f.get("geometry"))
                records.append({
                    "signal": signal,
                    "status": status,
                    "decision": a.get("decision"),
                    "ram_id": a.get("ram_id"),
                    "date_received": pd.to_datetime(a.get("d_date_rec"), unit="ms", errors="coerce"),
                    "address": address,
                    "use": use,
                    "looks_like_complex": bool(COMPLEX_HINT.search(use)),
                    "lat": lat,
                    "lng": lng,
                    "hex": h3.latlng_to_cell(lat, lng, H3_RES) if lat else None,
                })
    # One application can cover several parcels; keep one row per application.
    df = pd.DataFrame(records).drop_duplicates(subset=["signal", "address", "use", "date_received"])
    df = df[~df.decision.fillna("").str.contains(BAD_DECISIONS)]
    df = df[~df.address.str.contains("WITHDRAWN", case=False)]

    # Priority: STA beats dual-occ/secondary; recent beats old; complexes go to the body-corp pitch.
    order = {"short_term_accommodation": 0, "dual_occupancy": 1, "secondary_dwelling": 2}
    df["priority"] = df.signal.map(order)
    df["pitch"] = df.apply(
        lambda r: "body corporate / complex" if r.looks_like_complex else "To the Owner letter", axis=1
    )
    df = df.sort_values(["priority", "date_received"], ascending=[True, False]).drop(columns="priority")
    df.to_csv(OUT / "council_da_targets.csv", index=False)
    print(df.groupby(["signal", "pitch"]).size())
    print(f"Wrote {len(df)} rows to outputs/council_da_targets.csv")


if __name__ == "__main__":
    main()
