# Bin Caddie lead engine: Phase 0 (manual MVP)

The goal of Phase 0 is to prove the lead plan works before building software. **The test passes with 3 or more manager meetings and 1 or more signed pilot.**
Background is in `reports/Bin Caddie lead engine master plan.md`.

## What's here

| Path | What it is |
|---|---|
| `scripts/01_inside_airbnb.py` | Ranks every host, scores fit for Bin Caddie, and builds the density hexes and map |
| `scripts/02_council_das.py` | Pulls council short-term accommodation, dual-occupancy and secondary-dwelling approvals, with names stripped |
| `scripts/03_letterbox_flyers.py` | Picks 3 drop zones and generates a tracked DL flyer for each, with its own QR code and quote code |
| `scripts/04_build_workbook.py` | Builds `outputs/Phase0_Workbook.xlsx`, the working file for everything below |
| `scripts/research_brief.md` | Rules and fields used to research published business contacts for the top 40 managers |
| `outreach/email_sequences.md` | Three email angles (A, B, C) with follow-ups and a Spam Act checklist |
| `outreach/call_script.md` | Manager follow-up call, with objection handling |
| `mail/to_the_owner_letter.md` | Letter to properties approved by council for short-term accommodation |
| `field/noosa_sign_survey.md` | How to map which agency manages which street from Noosa's property signs |

`data/` and `outputs/` are **gitignored**. Inside Airbnb data must not be republished, and the outputs hold contact details. Regenerate them locally:

```bash
pip install pandas requests h3 qrcode openpyxl reportlab
curl -o data/raw/listings.csv.gz https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/data/listings.csv.gz
python3 scripts/01_inside_airbnb.py
python3 scripts/02_council_das.py
python3 scripts/03_letterbox_flyers.py
python3 scripts/04_build_workbook.py     # merges data/raw/accounts_batch_*.csv if present
```

## Phase 0 checklist (2 weeks)

| # | Task | Status | Where |
|---|---|---|---|
| 1 | Rank hosts by listing count | **Done**: 63 hosts with 10+ active listings run 36% of active listings | Workbook → *Accounts*, *Tier B Hosts*; `outputs/hex_map.html` |
| 2 | Research top 40 managers (published contacts) | **Done**: 30 contactable, 9 individuals or unidentified (not contacted), sister brands grouped (e.g. Alloggio Group, about 250 listings) | Workbook → *Accounts*; `outputs/wave1_email_drafts.md` |
| 3 | Pull council DA data | **Done**: 255 short-term accommodation approvals (53 complexes), plus ~800 dual-occupancy/secondary-dwelling approvals since 2023 | Workbook → *Council DA Targets* |
| 3b | Confirm Noosa's current bin and kerbside wording in the short-stay approval conditions | **You**: download the current conditions from noosa.qld.gov.au/short-stay-letting, or call Council | Changes Angle B wording |
| 4 | Noosa sign survey, one route | **Field** | `field/noosa_sign_survey.md`, Workbook → *Noosa Sign Log* |
| 5 | Test 3 angles on 15 managers | **Ready to send**: 15 personalised drafts (14 email, 1 phone-first) | `outputs/wave1_email_drafts.md`, `outreach/` |
| 6 | 2,000-letterbox drop with QR codes | **Flyers ready** (zones SB1, CB1, MK1) | `mail/flyer_*_DRAFT.pdf`, Workbook → *Letterbox Drops* |
| 6b | "To the Owner" letters, first 50 approvals | **Ready** | `mail/to_the_owner_letter.md` |
| 7 | Score it | Auto | Workbook → *Dashboard* |

## Bin Caddie must confirm before anything goes out
- Trial size for managers (templates say "3–5 homes, 2 weeks free") and any portfolio price.
- Flyer and letter wording, branding and logo. The flyers are drafts in neutral colours.
- Who sends emails and makes calls, and from which mailbox.
- The Turbo's Wheelie Clean arrangement before pitching cleaning (Angle C).

## Compliance (short version)
- **Email:** published business addresses only, with the source URL logged. Must be relevant to their role, identify Bin Caddie, and include an unsubscribe.
- **Calls:** business landlines only, weekdays 9am–8pm, Saturdays 9am–5pm, never Sundays. Show caller ID. Wash any mobile against the Do Not Call Register.
- **Never:** message hosts through Airbnb, scrape Airbnb, send cold SMS, contact individual hosts by name, or mention bins being left out.
- **Mail:** respect "No Junk Mail" signs. Address letters to "The Owner" only.
- This is general information, not legal advice. Get a lawyer to check before scaling up.
