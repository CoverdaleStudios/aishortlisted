"""Step 3: pick Phase 0 letterbox-drop zones and generate a tracked flyer for each.

Input : outputs/hexes_ranked.csv (from step 1)
Output: outputs/drop_plan.csv
        mail/flyer_<CODE>_DRAFT.pdf   - DL flyer (99 x 210 mm) with a zone-specific QR + promo code

Each zone gets its own QR (UTM-tagged, tracked by Bin Caddie's existing Google Analytics)
and its own phone code, so the Workbook can calculate leads and cost per zone.
Flyers are DRAFTS until Bin Caddie approves the wording, price and trial offer.
"""
from pathlib import Path

import pandas as pd
import qrcode
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT, MAIL = ROOT / "outputs", ROOT / "mail"
MAIL.mkdir(exist_ok=True)

ZONES = 3                 # ~650-700 letterboxes per zone = ~2,000 total
LETTERBOXES_PER_ZONE = 700
LANDING = "https://bincaddie.com.au/holiday-rental-bin-service"
# Coastal suburbs only: hinterland listings are too spread out for an efficient bin route.
COASTAL = {
    "Noosa Heads", "Noosaville", "Sunshine Beach", "Tewantin", "Peregian Beach - Marcus Beach",
    "Peregian Springs", "Coolum Beach", "Marcoola - Mudjimba", "Maroochydore - Kuluin",
    "Mooloolaba - Alexandra Headland", "Buddina - Minyama", "Parrearra - Warana",
    "Wurtulla - Birtinya", "Aroona - Currimundi", "Moffat Beach - Battery Hill",
    "Caloundra - Kings Beach", "Golden Beach - Pelican Waters", "Caloundra West - Baringa",
}

NAVY, GREEN, GREY = HexColor("#16324F"), HexColor("#2E9E5B"), HexColor("#5B6770")


def suburb_code(suburb: str, n: int) -> str:
    letters = "".join(w[0] for w in suburb.replace("-", " ").split())[:3].upper()
    return f"{letters}{n}"


def make_qr(url: str):
    img = qrcode.make(url, box_size=10, border=1)
    return ImageReader(img.get_image())


def flyer(path: Path, code: str, url: str) -> None:
    W, H = 99 * mm, 210 * mm
    c = canvas.Canvas(str(path), pagesize=(W, H))
    c.setTitle(f"Bin Caddie letterbox flyer {code}")
    # Header band
    c.setFillColor(NAVY)
    c.rect(0, H - 62 * mm, W, 62 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(8 * mm, H - 12 * mm, "BIN CADDIE")
    c.setFont("Helvetica", 8)
    c.drawString(8 * mm, H - 17 * mm, "Local, family run · Caloundra to Noosa")
    c.setFont("Helvetica-Bold", 21)
    for i, line in enumerate(["Holiday rental?", "We'll handle", "the bins."]):
        c.drawString(8 * mm, H - (31 + i * 9) * mm, line)

    # Body
    y = H - 74 * mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(8 * mm, y, "Guests forget. Neighbours notice.")
    c.setFont("Helvetica", 9)
    c.setFillColor(GREY)
    c.drawString(8 * mm, y - 5 * mm, "We put your bins out before council collection")
    c.drawString(8 * mm, y - 9.5 * mm, "and bring them back in after. Every week.")

    y -= 20 * mm
    bullets = [
        "2 visits a week, up to 4 bins",
        "Time- and location-stamped photo every visit",
        "No lock-in contracts, cancel anytime",
        "Bin cleaning & rubbish removal available",
    ]
    for b in bullets:
        c.setFillColor(GREEN)
        c.circle(10 * mm, y + 1.2 * mm, 1.3 * mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 9)
        c.drawString(14 * mm, y, b)
        y -= 6.5 * mm

    # Price block
    y -= 4 * mm
    c.setFillColor(HexColor("#EAF6EF"))
    c.roundRect(6 * mm, y - 20 * mm, W - 12 * mm, 24 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(10 * mm, y - 9 * mm, "$80")
    c.setFont("Helvetica", 9)
    c.drawString(30 * mm, y - 5 * mm, "per month (ex GST)")
    c.drawString(30 * mm, y - 9.5 * mm, "per holiday home")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(GREEN)
    c.drawString(10 * mm, y - 16.5 * mm, "2-week FREE trial for holiday rentals*")

    # QR + contact
    qr_size = 30 * mm
    c.drawImage(make_qr(url), 8 * mm, 14 * mm, qr_size, qr_size)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(42 * mm, 38 * mm, "Scan for a quote")
    c.setFont("Helvetica", 9)
    c.drawString(42 * mm, 32.5 * mm, "or call 0418 475 510")
    c.drawString(42 * mm, 27.5 * mm, "bincaddie.com.au")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(GREEN)
    c.drawString(42 * mm, 20 * mm, f"Quote code: {code}")
    c.setFont("Helvetica", 6)
    c.setFillColor(GREY)
    c.drawString(8 * mm, 8 * mm, "*On a long-term plan. Prices ex GST. ABN 39 174 579 656.")
    c.drawString(8 * mm, 5 * mm, "Delivered to letterboxes without 'No Junk Mail' signs.")
    c.showPage()
    c.save()


def main() -> None:
    hx = pd.read_csv(OUT / "hexes_ranked.csv")
    hx = hx[hx.suburb.isin(COASTAL)].sort_values(["self_managed_houses", "houses"], ascending=False)
    zones = hx.head(ZONES).copy()
    counts: dict[str, int] = {}
    rows = []
    for z in zones.itertuples():
        counts[z.suburb] = counts.get(z.suburb, 0) + 1
        code = suburb_code(z.suburb, counts[z.suburb])
        url = f"{LANDING}?utm_source=letterbox&utm_medium=flyer&utm_campaign=p0_{code.lower()}"
        pdf = MAIL / f"flyer_{code}_DRAFT.pdf"
        flyer(pdf, code, url)
        rows.append({
            "zone_code": code, "suburb": z.suburb, "hex": z.hex,
            "centre_map_link": f"https://www.google.com/maps/search/?api=1&query={z.lat:.5f},{z.lng:.5f}",
            "active_listings": z.active_listings, "houses": z.houses,
            "self_managed_houses": z.self_managed_houses,
            "target_letterboxes": LETTERBOXES_PER_ZONE, "qr_url": url, "flyer_pdf": pdf.name,
        })
    pd.DataFrame(rows).to_csv(OUT / "drop_plan.csv", index=False)
    print(pd.DataFrame(rows)[["zone_code", "suburb", "self_managed_houses", "flyer_pdf"]].to_string(index=False))


if __name__ == "__main__":
    main()
