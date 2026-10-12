# Bin Caddie Lead Engine

A local web app that holds every lead in one database. For each lead it shows a profile with sourced facts and a public-knowledge summary, writes personalised emails and letters from templates, checks each one for compliance, and delivers it through the email connector you choose. Nothing is sent until you approve it.

```
Phase 0 data ──► import ──► Accounts (businesses)  ─┐
 (Airbnb hosts,             Properties (addresses)  ├─► profile + facts + summary ─► template ─► compliance gate ─► Outbox ─► email provider / print
  research, council)        Owners (opted in only) ─┘          ▲                                                       │
                       enrich: website · ABN Lookup · Claude ──┘                         replies / unsubscribes ◄───────┘
```

## Quick start

**Easiest:** install Python 3 from python.org, then double-click `Start Lead Engine (Windows).bat` or `Start Lead Engine (Mac).command` (on a Mac, right-click → Open the first time). The first run installs what's needed, then your browser opens the dashboard.

**Manual:**

```bash
cd lead-engine
pip install -r requirements.txt
python -m leadengine.cli init
python -m leadengine.cli import        # needs ../bin-caddie-phase0 outputs (see its README)
python -m leadengine.cli hooks         # personalised opening lines
python -m leadengine.cli serve         # open http://127.0.0.1:5050
```

Then in **Settings**, set your sender name. Drafts can't be approved while it's still the `[Your name]` placeholder.

## What it does

| Area | What you get |
|---|---|
| **Accounts** | 48 business hosts plus 31 researched managers. Each shows its registered name (from ABN Lookup), trading name, group, portfolio (listings, houses, units, suburbs), pitch angle A/B/C, pipeline status and touch log. |
| **Contacts** | Each contact stores a name, role, email and phone, plus the **basis** you're allowed to contact them on: published by the business (with the URL where it's published), consent (with a timestamp and the wording they agreed to), or referral. |
| **Facts & summary** | Every fact keeps its source: Inside Airbnb, council open data, ABN Lookup, the business's own website, desk research, or the owner's own form. The summary is built from those facts, by Claude if configured, otherwise by built-in rules. |
| **Templates** | Seven starters: three email angles, two follow-ups, an owner reply and a "To the Owner" letter. They use merge fields such as `{{ greeting_name }}`, `{{ account.registered_name }}`, `{{ portfolio.suburbs }}` and `{{ hook }}`. Edit them with a live preview against a real account. |
| **Bulk drafts** | Writes one personalised draft per eligible account, matched to its angle. Sister brands (e.g. the Alloggio Group) get one draft between them. Accounts that publish only a phone number are skipped and listed so you can call instead. |
| **Compliance gate** | Blocks approval or sending if any of these apply: no source URL for a published address; a private owner who hasn't opted in; the recipient is on the suppression list; a "no marketing" notice; no unsubscribe; no sender ID; a leftover `[PLACEHOLDER]`; or the daily cap is reached. It also shows the legal calling window for phone follow-ups. |
| **Properties** | 1,051 council-approved addresses (short-term accommodation, dual occupancy, secondary dwellings) with local short-stay density. You can queue and print "To the Owner" letters. |
| **Owner form** (`/capture`) | The QR codes on flyers and letters point here. An owner gives their name, email, address, number of bins and collection day, and ticks consent. They become a full lead whose contact basis is consent. |
| **Outbox** | Draft → approve → deliver. Every send is logged as a touch, and an unsubscribe adds the contact to suppression on every channel. CSV export of all accounts is available. |

## About owners' names, addresses and emails

The system does build full records with **name + address + email** for private owners, but **only once the owner has given them**: through the owner form, a reply to a letter, or a referral. Until then a property is an address plus public facts, and contact is a letter addressed to "The Owner".

It deliberately does **not** compile private owners' names and emails from other sources:
- **Airbnb host profiles:** Airbnb's terms ban scraping and using members' details for commercial messages.
- **Valuer-General / title data** (CoreLogic, Pricefinder and similar): Queensland's code bans using it for direct marketing.
- **Council application names:** the importer strips them.

Cold emailing private individuals also breaches the Spam Act, and as the seller of the software you'd carry Privacy Act exposure. Keeping to this line is what lets you sell the system as compliant.

Businesses are different. Managers and agencies publish their contact details for enquiries, and those details are stored with the URL where they were found.

## Connecting email later

Settings → `email_provider`:

| Setting | What happens |
|---|---|
| `outbox` (default) | Nothing is sent. Approved emails are saved as `.eml` files in `exports/outbox/`. Double-click one to open it as a ready-to-send draft in Outlook or Apple Mail. |
| `smtp` | Sends from any mailbox: Google Workspace (`smtp.gmail.com:587`, using an app password), Microsoft 365 (`smtp.office365.com:587`), or your web host. Set `smtp_host`, `smtp_username` and `smtp_from` in Settings. The password goes in the `LEADENGINE_SMTP_PASSWORD` environment variable and is never stored in the database. |
| `gmail` / `outlook` | Placeholders for OAuth connectors (Gmail API / Microsoft Graph). These add reading replies automatically, and are the next build step once you pick a mailbox. |

Send from a **separate sending domain or subdomain** (e.g. `hello@getbincaddie.com.au`) with SPF, DKIM and DMARC set up, and stay under the daily cap (20 by default). That protects bincaddie.com.au's reputation.

## Enrichment

| Feature | How |
|---|---|
| **Website** | The *Read their website* button, or `cli enrich-web`. Reads up to 6 pages on the business's own domain, respects robots.txt, collects on-domain emails, phones and service mentions, and flags "no marketing" notices. It refuses to crawl platform sites (Airbnb, Stayz, Booking.com, LinkedIn, Facebook). |
| **ABN Lookup** | Get a free GUID at abr.business.gov.au → Web services, then paste it into Settings → `abr_guid`. Fills the registered entity name, ABN, status, GST and state/postcode. Check each match is the right entity. |
| **Claude** | Set `ANTHROPIC_API_KEY` and a Claude model ID (Settings → `llm_model`, or the `LEADENGINE_LLM_MODEL` environment variable). Summaries and hooks are then written by Claude using only the stored facts. Without them, built-in rules are used. |

## Tests

```bash
python -m pytest -q tests
```

Covers every page rendering; compose → approve → export; the gate blocking unsourced, suppressed and placeholder emails; private owners blocked without consent; the owner form recording consent; letters; the Phase 0 import skipping individuals; and calling hours.

## Data & privacy

- `instance/leads.db`, `exports/` and all imported data are **gitignored**. Keep the database on an encrypted laptop or server.
- A privacy policy must say what's collected, why, and how to opt out. From 10 Dec 2026 it must also cover automated decisions, which applies to the AI summaries.
- This is general information, not legal advice. Have a lawyer review it before selling the product.
