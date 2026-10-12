"""ABN Lookup (Australian Business Register) - the 'registered name' of a business.

Free web services, but you need a GUID: register at
https://abr.business.gov.au/Tools/WebServices and paste it into Settings -> abr_guid.
Endpoints return JSONP (callback(...)), which is unwrapped here.
"""
import json
import re

import requests

from .. import db

BASE = "https://abr.business.gov.au/json"
HEADERS = {"User-Agent": "BinCaddieLeadEngine/0.1 (+admin@bincaddie.com.au)"}


def _jsonp(text: str) -> dict:
    m = re.search(r"^\s*\w*\((.*)\)\s*;?\s*$", text, re.S)
    return json.loads(m.group(1) if m else text)


def search_names(name: str, guid: str, max_results: int = 5) -> list[dict]:
    r = requests.get(f"{BASE}/MatchingNames.aspx",
                     params={"name": name, "maxResults": max_results, "guid": guid},
                     headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = _jsonp(r.text)
    if data.get("Message"):
        raise RuntimeError(data["Message"])
    return data.get("Names") or []


def abn_details(abn: str, guid: str) -> dict:
    r = requests.get(f"{BASE}/AbnDetails.aspx", params={"abn": re.sub(r"\D", "", abn), "guid": guid},
                     headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = _jsonp(r.text)
    if data.get("Message"):
        raise RuntimeError(data["Message"])
    return data


def enrich_account(conn, account, guid: str) -> str:
    """Find the best ABN match for the trading name (QLD first) and store the registered details."""
    if not guid:
        return "No ABR GUID set (Settings -> abr_guid)."
    query = account["trading_name"] or account["display_name"]
    names = search_names(query, guid)
    names = sorted(names, key=lambda n: (n.get("State") != "QLD", -(n.get("Score") or 0)))
    if not names:
        return f"No ABN match for '{query}'."
    best = names[0]
    d = abn_details(best["Abn"], guid)
    business_names = d.get("BusinessName") or []
    gst = "yes" if d.get("Gst") else "no"
    conn.execute(
        """UPDATE accounts SET abn = ?, registered_name = ?, entity_type = ?, abn_status = ?, gst_registered = ?,
               abn_state = ?, abn_postcode = ?, updated_at = ? WHERE id = ?""",
        (d.get("Abn"), d.get("EntityName"), d.get("EntityTypeName"), d.get("AbnStatus"), gst,
         d.get("AddressState"), d.get("AddressPostcode"), db.now(), account["id"]),
    )
    url = f"https://abr.business.gov.au/ABN/View?abn={d.get('Abn')}"
    db.add_fact(conn, f"ABN {d.get('Abn')} ({d.get('AbnStatus')}) - {d.get('EntityName')}, "
                      f"{d.get('EntityTypeName')}, {d.get('AddressState')} {d.get('AddressPostcode')}; GST {gst}.",
                account_id=account["id"], topic="registration", source_name="ABN Lookup", source_url=url)
    if business_names:
        db.add_fact(conn, "Registered business names on this ABN: " + ", ".join(business_names) + ".",
                    account_id=account["id"], topic="registration", source_name="ABN Lookup", source_url=url)
    match_note = f"matched '{best.get('Name')}' (score {best.get('Score')})"
    return f"Stored ABN {d.get('Abn')} - {d.get('EntityName')} ({match_note}). Check it is the right entity."
