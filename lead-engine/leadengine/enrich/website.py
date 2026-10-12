"""Read a business's OWN website for published contact details and owner-services facts.

Polite by design: honours robots.txt, identifies itself, reads at most a handful of pages
on the same domain, and records the exact URL each detail came from (Spam Act evidence).
Only ever pointed at business websites - never at Airbnb or other platforms whose terms
prohibit scraping.
"""
import re
import time
from urllib import robotparser
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .. import db

UA = "BinCaddieLeadEngine/0.1 (+admin@bincaddie.com.au)"
BLOCKED_HOSTS = ("airbnb.", "stayz.", "booking.com", "expedia.", "vrbo.", "linkedin.", "facebook.", "instagram.")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+61\s?|0)[2-478](?:[\s-]?\d){8}|1[38]00(?:[\s-]?\d){6}")
NO_MARKETING = re.compile(r"no (?:unsolicited|marketing|sales|spam)|do not (?:send|contact).{0,30}(?:marketing|sales)|"
                          r"not wish to receive (?:marketing|sales)", re.I)
SERVICE_WORDS = ("cleaning", "linen", "laundry", "garden", "pool", "pest", "maintenance", "bins", "waste", "rubbish")
CONTACT_HINTS = re.compile(r"contact|about|team|owner|list|manage|services", re.I)
MAX_PAGES = 6


def _allowed(rp: robotparser.RobotFileParser, url: str) -> bool:
    try:
        return rp.can_fetch(UA, url)
    except Exception:
        return True


def crawl(start_url: str) -> list[tuple[str, str]]:
    if not start_url.startswith("http"):
        start_url = "https://" + start_url
    host = urlparse(start_url).netloc
    if any(b in host for b in BLOCKED_HOSTS):
        raise ValueError(f"{host} is a platform site - not crawled (terms of service).")
    rp = robotparser.RobotFileParser(f"https://{host}/robots.txt")
    try:
        rp.read()
    except Exception:
        pass
    pages, queue, seen = [], [start_url], set()
    while queue and len(pages) < MAX_PAGES:
        url = queue.pop(0)
        if url in seen or not _allowed(rp, url):
            continue
        seen.add(url)
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
        except requests.RequestException:
            continue
        if r.status_code != 200 or "html" not in r.headers.get("content-type", ""):
            continue
        pages.append((url, r.text))
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"]).split("#")[0]
            if urlparse(link).netloc == host and link not in seen and CONTACT_HINTS.search(link + a.get_text(" ")):
                queue.append(link)
        time.sleep(1)
    return pages


def enrich_account(conn, account) -> str:
    site = account["website"]
    if not site:
        return "No website on the account."
    pages = crawl(site)
    if not pages:
        return "Could not read the website (blocked by robots.txt or unreachable)."
    domain = urlparse(pages[0][0]).netloc.removeprefix("www.")
    found_emails, found_phones, no_marketing = {}, {}, False
    services = set()
    for url, html in pages:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select('a[href^="mailto:"]'):
            e = a["href"][7:].split("?")[0].strip().lower()
            found_emails.setdefault(e, url)
        text = soup.get_text(" ", strip=True)
        for e in EMAIL_RE.findall(text):
            found_emails.setdefault(e.lower(), url)
        for p in PHONE_RE.findall(text):
            found_phones.setdefault(re.sub(r"\s+", " ", p.strip()), url)
        if NO_MARKETING.search(text):
            no_marketing = True
            db.add_fact(conn, "Website carries a 'no marketing / no sales' notice.", account_id=account["id"],
                        topic="web", source_name="Business website", source_url=url)
        lower = text.lower()
        services |= {w for w in SERVICE_WORDS if w in lower}
        title = soup.title.get_text(strip=True) if soup.title else ""
        desc = soup.find("meta", attrs={"name": "description"})
        if url == pages[0][0] and (title or desc):
            db.add_fact(conn, f"Website: {title}. {desc['content'] if desc and desc.get('content') else ''}".strip(),
                        account_id=account["id"], topic="web", source_name="Business website", source_url=url)

    # Only keep addresses on the business's own domain (avoids web-designer / platform addresses).
    own = {e: u for e, u in found_emails.items() if e.split("@")[-1].removeprefix("www.").endswith(domain)}
    for e, u in own.items():
        db.upsert_contact(conn, account["id"], email=e, basis="published_business", source_url=u)
    for p, u in list(found_phones.items())[:3]:
        db.upsert_contact(conn, account["id"], phone=p, basis="published_business", source_url=u)
    if services:
        db.add_fact(conn, "Website mentions: " + ", ".join(sorted(services)) + ".", account_id=account["id"],
                    topic="services", source_name="Business website", source_url=pages[0][0])
    conn.execute("UPDATE accounts SET no_marketing_notice = ?, updated_at = ? WHERE id = ?",
                 ("yes" if no_marketing else "no", db.now(), account["id"]))
    return (f"Read {len(pages)} page(s): {len(own)} on-domain email(s), {len(found_phones)} phone(s)"
            + ("; NO-MARKETING notice found - email blocked." if no_marketing else "."))
