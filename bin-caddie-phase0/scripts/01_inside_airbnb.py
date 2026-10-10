"""Step 1: rank Sunshine Coast / Noosa short-stay hosts and map listing density.

Input : data/raw/listings.csv.gz  (Inside Airbnb, Sunshine Coast scrape)
Output: outputs/hosts_ranked.csv      - every host with 2+ active listings, tiered
        outputs/hexes_ranked.csv      - H3 hexes ranked by active bin-relevant houses
        outputs/suburbs_summary.csv   - per-suburb counts for letterbox planning
        outputs/hex_map.html          - Leaflet heat map of the hexes

Inside Airbnb data is used for internal analysis only - do not republish it.
Coordinates are offset by Airbnb (~150 m), so hexes use H3 resolution 8 (~460 m edge).
"""
import json
import re
import sys
from pathlib import Path

import h3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "listings.csv.gz"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

SNAPSHOT = pd.Timestamp("2026-09-28")
H3_RES = 8

# Property types that normally have their own kerbside wheelie bins.
HOUSE_TYPES = {
    "Entire home", "Entire townhouse", "Entire cottage", "Entire villa",
    "Entire vacation home", "Entire bungalow", "Entire cabin", "Tiny home",
    "Farm stay", "Entire place", "Entire chalet", "Entire home/apt",
}
# Apartments usually share a bin room run by a body corporate / on-site manager.
UNIT_TYPES = {
    "Entire rental unit", "Entire serviced apartment", "Entire condo",
    "Entire loft", "Room in aparthotel", "Room in serviced apartment",
}

# Words that suggest a host name is a business rather than a private person.
BUSINESS_WORDS = re.compile(
    r"holiday|holidays|property|properties|management|stays?|rentals?|accom|"
    r"realty|real estate|group|resort|retreats?|co\b|pty|noosa|coast|caloundra|"
    r"coolum|mooloolaba|maroochy|beach|team|hosts?|homes|living|escapes?|"
    r"apartments|villas|collection|ready|bnb|getaways?|letting",
    re.I,
)


def classify_property(ptype: str) -> str:
    if ptype in HOUSE_TYPES:
        return "house"
    if ptype in UNIT_TYPES:
        return "unit"
    return "on_host_site"  # guest suites, guesthouses, private rooms


def main() -> None:
    if not RAW.exists():
        sys.exit(f"Missing {RAW}. Download it first (see README).")

    df = pd.read_csv(RAW, low_memory=False)
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")
    df["active"] = (df["number_of_reviews_ltm"].fillna(0) > 0) | (
        df["last_review"] >= SNAPSHOT - pd.Timedelta(days=365)
    )
    df["prop_class"] = df["property_type"].fillna("").map(classify_property)
    df["hex"] = [h3.latlng_to_cell(la, lo, H3_RES) for la, lo in zip(df.latitude, df.longitude)]

    act = df[df.active]
    print(f"Listings: {len(df):,}  active: {len(act):,}  hosts: {df.host_id.nunique():,}")

    # ---- Hosts -------------------------------------------------------------
    g = act.groupby("host_id")
    hosts = pd.DataFrame({
        "host_name": g.host_name.first(),
        "host_url": g.host_url.first(),
        "host_since": g.host_since.first(),
        "airbnb_total_listings": g.host_total_listings_count.max(),
        "active_listings_here": g.size(),
        "houses": g.prop_class.apply(lambda s: (s == "house").sum()),
        "units": g.prop_class.apply(lambda s: (s == "unit").sum()),
        "on_host_site": g.prop_class.apply(lambda s: (s == "on_host_site").sum()),
        "top_suburbs": g.neighbourhood_cleansed.apply(
            lambda s: "; ".join(f"{k} ({v})" for k, v in s.value_counts().head(4).items())
        ),
        "hexes": g.hex.nunique(),
        "est_revenue_l365d": g.estimated_revenue_l365d.sum(),
    }).reset_index()
    hosts = hosts[hosts.active_listings_here >= 2]

    hosts["looks_like_business"] = hosts.host_name.fillna("").str.contains(BUSINESS_WORDS)
    hosts["tier"] = pd.cut(
        hosts.active_listings_here, [1, 4, 9, 10_000], labels=["B- (2-4)", "B (5-9)", "A (10+)"]
    )
    # Bin Caddie fit: houses are the core product; units point to a body-corp pitch.
    hosts["bin_fit_score"] = hosts.houses * 1.0 + hosts.units * 0.4 + hosts.on_host_site * 0.1
    hosts["pitch"] = hosts.apply(
        lambda r: "holiday-home valet" if r.houses >= r.units else "body corporate / bin room",
        axis=1,
    )
    # Individuals are NOT contacted by name (Spam Act / Airbnb terms). Mark them.
    hosts["outreach_route"] = hosts.apply(
        lambda r: "named B2B outreach" if (r.looks_like_business or r.active_listings_here >= 10)
        else "research business identity first; else geo/inbound only",
        axis=1,
    )
    hosts = hosts.sort_values(["active_listings_here", "bin_fit_score"], ascending=False)
    hosts.to_csv(OUT / "hosts_ranked.csv", index=False)

    a = hosts[hosts.active_listings_here >= 10]
    print(f"Hosts 10+: {len(a)} controlling {a.active_listings_here.sum():,} active listings "
          f"({a.active_listings_here.sum() / len(act):.0%})")

    # ---- Hexes -------------------------------------------------------------
    hx = act.groupby("hex").agg(
        active_listings=("id", "size"),
        houses=("prop_class", lambda s: (s == "house").sum()),
        units=("prop_class", lambda s: (s == "unit").sum()),
        managed_by_10plus=("calculated_host_listings_count", lambda s: (s >= 10).sum()),
        suburb=("neighbourhood_cleansed", lambda s: s.value_counts().index[0]),
    ).reset_index()
    hx["self_managed_houses"] = act[(act.prop_class == "house") & (act.calculated_host_listings_count < 5)] \
        .groupby("hex").size().reindex(hx.hex).fillna(0).astype(int).values
    hx["lat"], hx["lng"] = zip(*[h3.cell_to_latlng(c) for c in hx.hex])
    # Letterbox score: self-managed houses are the Tier C (letterbox) audience.
    hx = hx.sort_values(["self_managed_houses", "houses"], ascending=False)
    hx.to_csv(OUT / "hexes_ranked.csv", index=False)

    # ---- Suburbs -----------------------------------------------------------
    sub = act.groupby("neighbourhood_cleansed").agg(
        active_listings=("id", "size"),
        houses=("prop_class", lambda s: (s == "house").sum()),
        units=("prop_class", lambda s: (s == "unit").sum()),
        hosts=("host_id", "nunique"),
    )
    sub["self_managed_houses"] = act[(act.prop_class == "house") & (act.calculated_host_listings_count < 5)] \
        .groupby("neighbourhood_cleansed").size().reindex(sub.index).fillna(0).astype(int)
    sub.sort_values("self_managed_houses", ascending=False).to_csv(OUT / "suburbs_summary.csv")

    write_map(hx)
    print("Wrote hosts_ranked.csv, hexes_ranked.csv, suburbs_summary.csv, hex_map.html")


def write_map(hx: pd.DataFrame) -> None:
    feats = []
    for r in hx.itertuples():
        ring = [[lng, lat] for lat, lng in h3.cell_to_boundary(r.hex)]
        ring.append(ring[0])
        feats.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [ring]},
            "properties": {
                "hex": r.hex, "suburb": r.suburb, "active": int(r.active_listings),
                "houses": int(r.houses), "units": int(r.units),
                "self": int(r.self_managed_houses), "managed10": int(r.managed_by_10plus),
            },
        })
    geo = json.dumps({"type": "FeatureCollection", "features": feats})
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bin Caddie STR density map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body,#m{{height:100%;margin:0;font-family:system-ui,sans-serif}}
#k{{position:absolute;z-index:999;top:10px;right:10px;background:#fff;padding:10px 12px;border-radius:8px;
box-shadow:0 1px 6px #0003;font-size:13px;max-width:260px}}
select{{margin-top:6px;width:100%}}</style></head><body><div id="m"></div>
<div id="k"><b>Short-stay density (H3 ~460 m)</b><br>Colour by:
<select id="f"><option value="self">Self-managed houses (letterbox targets)</option>
<option value="houses">All houses</option><option value="units">Units (body corp)</option>
<option value="managed10">Listings run by 10+ hosts</option><option value="active">All active listings</option></select>
<div style="margin-top:6px;color:#555">Source: Inside Airbnb 28 Sep 2026, internal use only. Locations offset ~150 m.</div></div>
<script>
const data={geo};
const m=L.map('m').setView([-26.6,153.05],11);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'&copy; OpenStreetMap'}}).addTo(m);
let layer;
function col(v,max){{const t=Math.min(1,v/max);return `rgba(${{Math.round(255*t)}},${{Math.round(140*(1-t))}},60,${{0.15+0.65*t}})`;}}
function draw(){{const f=document.getElementById('f').value;
 const max=Math.max(...data.features.map(x=>x.properties[f]))||1;
 if(layer) m.removeLayer(layer);
 layer=L.geoJSON(data,{{style:x=>({{weight:0.5,color:'#333',fillColor:col(x.properties[f],max*0.6),fillOpacity:1}}),
 onEachFeature:(x,l)=>{{const p=x.properties;l.bindPopup(`<b>${{p.suburb}}</b><br>Active listings: ${{p.active}}<br>Houses: ${{p.houses}} (self-managed ${{p.self}})<br>Units: ${{p.units}}<br>Run by 10+ hosts: ${{p.managed10}}<br><small>${{p.hex}}</small>`)}}}}).addTo(m);}}
document.getElementById('f').onchange=draw;draw();
</script></body></html>"""
    (OUT / "hex_map.html").write_text(html)


if __name__ == "__main__":
    main()
