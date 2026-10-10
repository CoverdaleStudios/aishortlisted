# Bin Caddie lead engine: master plan

*A plan for an AI lead generation system, first built for Bin Caddie and then sold to other short-stay service businesses. Facts are current to 10 October 2026. This is not legal advice. Have a lawyer check the compliance layer before you sell it.*

---

## 1. Why you don't need to find Airbnb owners

The brief assumes the hard part is finding individual Airbnb owners, because Airbnb hides who they are. The data shows that most of the market can be reached without ever identifying them.

**The market is concentrated.** The 28 September 2026 Inside Airbnb dataset for Sunshine Coast and Noosa has 7,315 listings from 3,195 hosts:

- **87 hosts with 10 or more listings control 2,911 listings, about 40%.**
- Another **97 hosts have 5–9 listings**.
- The largest are Welcome Ready Holiday Homes (191), Caloundra Holiday Centre (128), Team Tabi (116), Niche Holidays Noosa (112), Holiday Caloundra (92) and Aspire Property Management (91).

**These hosts are businesses.** Their names and listing counts are public on Airbnb. Their email addresses are published on their websites, and their offices are on Google Maps. Cold B2B outreach to them is lawful when done properly. One signed manager can be worth 20–190 properties.

**Treat the market as three tiers, each reached a different way:**

| Tier | Who | Approx. size | How you reach them | Value per win |
|---|---|---|---|---|
| **A. Managers** | Letting agencies, co-hosts, Noosa "contact persons", resort and on-site managers, body corporate managers | ~150–200 businesses covering ~3,000–4,000 listings | Named-account B2B outreach | 10–190 properties |
| **B. Small portfolio hosts** | Hosts with 2–9 listings, often trading under a business name | ~100–300 hosts | Business-name research, then any published business contact, plus partners | 2–9 properties |
| **C. Single-property owners** | Individuals who self-manage | ~2,500+ hosts | **Places, not people**: geo-targeted letterbox drops, street signals, inbound marketing, referrals | 1 property |

The software's job is to work Tier A by name, Tier B by research, and Tier C by geography and inbound marketing. It should never need a private person's identity that it isn't allowed to have. That is both the legally safe design and the commercially strongest one.

---

## 2. Rules the system must follow

These rules are built into the code, not left in a policy document. When you sell the product, this is what lets you say it won't get the buyer fined, which is a big part of what justifies charging thousands.

**Allowed**

- **Cold email to a manager's published business address**, under the Spam Act's "conspicuous publication" inferred consent. All of these must hold:
  - the address is published, and the system logs where it was found;
  - there is no "no marketing" notice next to it;
  - the offer is relevant to the recipient's role, which bin management for a letting manager is;
  - the email identifies the sender and has a working unsubscribe.
- **Calls to business landlines.** Business numbers can't be put on the Do Not Call Register, but the Telemarketing Standard still applies:
  - calls only 9am–8pm on weekdays and 9am–5pm on Saturdays, never on Sundays;
  - the caller identifies themselves at the start and shows a caller number;
  - **wash every mobile number against the Do Not Call Register before calling it.** Lead My Way paid $285,600 for skipping this.
- **Unaddressed letterbox drops** that respect "No Junk Mail" signs, and addressed mail to "The Owner". The Spam Act doesn't cover physical mail.
- **Google Places API** to find businesses. Store place IDs; cached coordinates expire after 30 days.
- **Video-only dashcam computer vision on public streets** for letterbox targeting. Queensland's Invasion of Privacy Act 1971 covers listening devices, not cameras. Keep audio off, blur faces and number plates, and keep only the address and a flag.

**Not allowed (the system blocks these)**

- **Scraping Airbnb, or pitching hosts through Airbnb messages.** Airbnb's Terms s 11.1 (updated 5 February 2026) ban scrapers and using members' details to send commercial messages. Treat Stayz, Booking.com and LinkedIn scraping the same way.
- **Cold SMS to hosts' mobile numbers.** Send SMS only after the person opts in.
- **Using Valuer-General owner names for direct marketing.** That data is sold through CoreLogic/RP Data, Pricefinder and others, and a Queensland code of conduct bars using it this way. Use it for internal market sizing only.
- **Telling people "we noticed your bins were left out".** Using street data in outreach would feel like surveillance and invites a privacy-tort claim. The statutory tort has applied to everyone since 10 June 2025.
- **AI-written fake reviews, testimonials or unsupported claims.** These breach the Australian Consumer Law; Service Seeking was ordered to pay $600,000.

**Privacy Act exposure.** Bin Caddie is probably under the $3m small business exemption. The exemption doesn't apply to a business that trades in personal information for a benefit, so **you, as the software vendor, should assume the Privacy Act applies to you**. The product therefore needs:

- a privacy policy;
- data minimisation, meaning it stores business contacts and not private individuals;
- an automated decision-making disclosure, required from 10 December 2026.

**Inside Airbnb.** The download page says CC BY 4.0, but the policies page asks people not to republish the data and states a housing-research mission. Use it internally for maps and market sizing. **Never resell it or show it raw to customers.** Each customer instance should pull it fresh, credited, for its own internal analysis. Get a lawyer's view before you scale the product.

---

## 3. System architecture

The system has eight modules. Modules 1, 2, 3 and 8 are the minimum product. Modules 4–7 are what make it worth thousands.

```
 DATA SOURCES ──► 1. Market Map ──► 2. Account Intelligence ──► 3. Compliant Outreach ──┐
 (Inside Airbnb,     (density heat-     (manager list, scoring,     (email, calls, mail,   │
  DA open data,       map, route fit)    AI research briefs)          tasks)               ▼
  Places API,                                                                       CRM / pipeline
  Noosa signs,     4. Street Signal ──► 5. Geo Mail ──────────────────────────────►  (GoHighLevel)
  co-host pages)      (field capture)    (letterbox + "Owner" mail)                        ▲
                   6. Inbound Engine (suburb pages, Google Business Profile, Meta ads, AI receptionist) ┤
                   7. Partner & Referral Engine (cleaners, linen, Turbo's, agents)  ───────┘
                   8. Conversion, Retention & Attribution (trial, photo proof, reviews, CAC/LTV)
```

### Module 1: Market Map
The base layer. It shows where the short-stay properties are and which of them Bin Caddie can serve profitably.

- **Inputs:**
  - Inside Airbnb listings: offset coordinates, host ID, host listing count, last review date, room type.
  - Sunshine Coast Council development-application open data: an ArcGIS REST endpoint licensed CC BY 3.0 AU. It has 314 short-term accommodation applications, 144 of them since 2023, plus dual occupancy and secondary dwelling applications.
  - Noosa's quarterly short-stay snapshots, by suburb.
- **Processing:**
  - Bucket listings into hexagons of about 300 m (H3 resolution 8–9).
  - Compute active-listing density per hexagon and per street.
  - Overlay Bin Caddie's existing customer stops and council collection days.
- **Output: a route-fit score for every area.** Bin valet profits depend on stop density: a new client on an existing Tuesday route in Noosaville is worth far more than an isolated one in the hinterland. Every lead in every other module inherits this score.
- **Bin-type filter.** About 2,438 of Noosa's 3,167 approvals are duplexes or units, which often use shared bins. Those leads go to a body corporate or on-site manager playbook, not the holiday-home playbook.

### Module 2: Account Intelligence (Tier A and B engine)
- **Build the named account list from:**
  - Inside Airbnb host names with 5 or more listings;
  - Airbtics' list of 46 ranked Sunshine Coast managers;
  - Airbnb Co-Host Network suburb pages, read manually; they're public profiles, but don't scrape them;
  - Tourism Noosa member directory, which has 550+ members;
  - Google Places API searches for "holiday letting", "property management", "body corporate management", "management rights" and "Airbnb management";
  - applicants named in the council development-application data, where they are businesses;
  - the Strata Community Association Qld directory, and management-rights broker listings such as ARAMA and Resort Brokers, which name buildings with on-site managers.
- **Entity resolution.** Merge the same business across sources, for example the Airbnb host "Niche Holidays Noosa" with its Google Business Profile and its website.
- **Enrichment.** Scrape the business's own website for its published email, phone, team page and listing count. Log the source URL of every contact, because it is your Spam Act proof. Apify's Google Maps scraper costs about US$1.50 per 1,000 places, and contact add-ons about US$0.002 each. Skip Clay until you have several customers.
- **Account score** combines:
  - estimated managed properties;
  - overlap with high route-fit hexagons;
  - property type (houses score higher than units with shared bins);
  - Noosa exposure, because of the contact-person duties;
  - growth signals: new listings, new development applications, hiring.
- **AI research brief.** An LLM writes a one-page brief per account: portfolio size and suburbs, likely pain points, the best opening angle, and the decision-maker's published name and role. This is cheap: a few cents per account on a low-cost model tier.

### Module 3: Compliant Outreach Orchestrator
A sequence engine with the rules from section 2 enforced in code.

- **Email.**
  - Personalised from the research brief, sent from a separate sending domain through Smartlead or Instantly (from about US$39–47 a month).
  - Every send is checked against: a logged published source, a role-relevance tag, an unsubscribe link, and a suppression list synced across all channels.
  - Volume stays low: 150–200 accounts don't need volume, they need relevance.
- **Calls.**
  - Tasks are generated only inside legal calling hours, with a Do Not Call Register wash before any mobile number is dialled.
  - An AI drafts the call script. A human, the owner of Bin Caddie, makes the call.
  - AI voice agents (about US$0.05–0.31 a minute) are used **only for inbound calls**, never cold calls.
- **Physical touch.** For the top 30 accounts, send a printed one-page portfolio proposal by mail. Include a map of their listings that fall in Bin Caddie's route zones, built from Module 1 and kept aggregated so no individual owner is identified. For example: "We already service 14 streets where you manage 38 homes."
- **Offer ladder:**
  1. A free 2-week pilot on 5 properties, with time-stamped photo proof sent to the manager.
  2. Portfolio pricing.
  3. A monthly compliance report.

### Module 4: Street Signal (field data capture)
This is the module that gives you data nobody else has. Bin Caddie's vehicles already drive these streets twice a week.

- **Noosa approval signs.** Every approved Noosa short-stay property must display a sign at the front, with letters at least 50 mm high, showing its approval number and the 24/7 local contact person.
  - A phone app or dashcam reads the sign with text recognition and stores the approval number, the contact name if it's a business, and the address.
  - **The contact person is usually a letting agent, so the signs map which agency manages which street.** Feed that into Module 2.
  - Individual contact persons' phone numbers are for complaints, not marketing. The system stores a hash and sends no outreach to them.
- **Bins-left-out detection (optional, phase 3).**
  - Video-only dashcam with an object-detection model (YOLO-class), trained on footage you collect and label yourself. Public wheelie-bin datasets are tiny, at 82–151 images.
  - The flag "bins still out more than 24 hours after collection" feeds only into the letterbox targeting list in Module 5. It never goes into a message.
- **Privacy controls:** no audio, faces and plates blurred on the device, raw footage deleted within 7 days, and only the address, flag and timestamp kept.

### Module 5: Geo Mail (Tier C engine)
- **Unaddressed mail by suburb or postcode** through Australia Post, aimed at the densest areas from Module 1.
  - About 40.5c per letterbox (standard 15-day service; 51.6c for 7-day premium), within Queensland, up to 50g.
  - A 5,000-letterbox wave costs about $2,000 in postage, plus printing.
  - Avoid the peak period from 2 November 2026 to 1 January 2027.
- **Hand-delivered micro-drops** by Bin Caddie's crews on streets that rank high for density and bins-left-out flags. The cost is close to zero because they are already there, and they must respect "No Junk Mail" signs.
- **Addressed "To the Owner" letters** to properties named in development applications for short-term accommodation. Use only the address, not the owner name from the application.
- **Measure every piece.** Each drop carries a unique QR code and short URL for each hex or campaign, so the system can calculate cost per lead by area and re-target the next wave.
- **The message is the host's problem, not the bins:** "Guests leave bins out, neighbours complain, Noosa issues compliance notices. $80 a month and it's handled, with photo proof." Only use the Noosa compliance claim once you've checked the current approval conditions. The "no more than 24 hours" bin wording comes from a 2021 draft and couldn't be confirmed in the current conditions.

### Module 6: Inbound Engine
- **Programmatic landing pages:** one page per suburb and use case, such as "holiday rental bin service Noosaville". The LLM drafts them and a human edits each one, so the pages hold real local detail: that suburb's collection days and council rules. Search engines don't reward thin generated pages.
- **Google Business Profile:** fix the gaps the earlier research found. Build up genuine reviews from pilot customers, post weekly, and add service-area suburbs.
- **Meta lead ads** aimed at Sunshine Coast and Noosa property owners interested in short-term rental hosting. The benchmark is about AUD $20–35 per lead.
- **Host communities:** join local host Facebook groups and Airbnb host meetups and answer questions honestly. Don't post spam.
- **AI receptionist:** web chat, missed-call text-back, a voice agent for after-hours calls, and the instant-quote calculator the site already has. A lead must get a reply within 5 minutes, at any hour.

### Module 7: Partner and Referral Engine
Holiday-rental owners already pay cleaners, linen services, pool and lawn contractors, and agents. Those suppliers are trusted, they visit the same properties, and they can make introductions.

- **Partner list:** STR cleaners, linen hire, Turbo's Wheelie Clean (already a partner), pest and pool services, real estate agents' rental departments, and management-rights brokers.
- **Partner portal:** a referral link per partner, automatic tracking, and a referral fee such as one month free or $50 per signed property.
- **Integrations, phase 3:** list Bin Caddie as a service partner in property-management-system marketplaces such as Hostaway and Guesty. Each lists 100–200+ partner apps, including cleaning tools like Breezeway and Turno.
  - Managers connect with an API key, and Bin Caddie reads checkout calendars to schedule extra bin runs after big turnovers.
  - That makes Bin Caddie much harder to cancel. For the product you sell, it's also a feature that is hard to copy.

### Module 8: Conversion, Retention and Attribution
- **Pilot flow:** booking, a 2-week trial, daily photo proof sent automatically to the manager, an automated day-10 check-in, and conversion to a plan.
- **Retention:**
  - a monthly report per property: visits, photos, issues;
  - churn-risk flags such as missed payments or fewer properties;
  - an offer to add bin cleaning, delivered with Turbo's.
- **Genuine review requests** after the third successful week, through the CRM. No incentives tied to positive reviews.
- **Attribution dashboard** for every channel, area and partner: cost per lead, cost to acquire a customer, conversion rate, payback period and lifetime value.

---

## 4. Unit economics

At $80 a month ex GST per property and an **assumed** 50% gross margin (Bin Caddie's real cost data would replace this):

| Monthly churn | Lifetime revenue (AUD) | Max acquisition cost at 3:1 LTV:CAC |
|---|---|---|
| 2% | $4,000 | ~$670 |
| 3% | $2,667 | ~$440 |
| 5% | $1,600 | ~$270 |

- **A manager deal with 20 properties is worth $32,000–80,000 in lifetime revenue.** You can spend hours of personal attention on each Tier A account.
- **Letterbox drops are worthwhile** if about 1 in 1,000–2,000 letterboxes converts. A 5,000-letterbox wave at about $2,000–2,500 including printing needs only 3–4 single-property customers to beat the acquisition-cost limit.
- **Running cost for one region:** about US$250–600 a month before ad spend and printing. That covers GoHighLevel, a cold-email tool, Apify or Places API calls, and LLM usage.

**What winning looks like for Bin Caddie in 12 months (illustrative, not a forecast):**

- 6 manager accounts averaging 20 properties = 120 properties;
- 2 body corporates;
- 80 single-property owners from mail and inbound.

That is about 200 serviced properties, roughly **$16,000+ a month ex GST** in recurring revenue. The real limit will be Bin Caddie's capacity to run routes, which is why Module 1's route-fit score matters.

---

## 5. Build roadmap

### Phase 0: Manual MVP (weeks 1–2). Proves the plan before you write code.
1. Download the Inside Airbnb Sunshine Coast `listings.csv.gz` (28 September 2026). Rank hosts by listing count and filter to those with 5 or more.
2. Research the top 40 by hand: website, published email, office phone, decision-maker, and portfolio suburbs.
3. Pull the council development-application data for short-term accommodation, dual occupancy and secondary dwellings since 2023.
4. Drive one Noosa route and photograph approval signs to map agencies to streets.
5. Write three outreach angles and test them on 15 managers by email, plus phone follow-ups.
6. Run one 2,000-letterbox drop with QR codes in the densest Noosaville or Noosa Heads hexes.
7. **Pass criteria:** 3 or more manager meetings and 1 or more pilots signed. That proves the thesis for Bin Caddie and gives you a case study to sell with.

### Phase 1: Core engine (weeks 3–8)
- **Data pipeline** (Python plus Postgres/PostGIS, or Supabase), on a schedule:
  - Inside Airbnb pulls each quarter;
  - development-application API pulls each week;
  - Places API refreshes each month.
- Entity resolution, account scoring, and AI research briefs.
- **GoHighLevel** as the CRM and sequencer: the US$297 plan for now, moving to the US$497 SaaS plan when you resell. Smartlead for cold email.
- **Compliance layer:** source logging, a suppression list across all channels, calling-hour guard, Do Not Call Register wash, and the scraping blocklist.
- A simple map dashboard (Mapbox or Leaflet) showing route-fit hexes and existing customers.

### Phase 2: Field and mail (weeks 9–14)
- A sign-capture phone app, with on-device text recognition and an address taken from GPS.
- A geo mail campaign builder: pick hexes, generate an Australia Post postcode plan, print-ready artwork, and QR codes.
- An inbound pack: generated suburb pages, the Google Business Profile playbook, Meta lead ads, and the AI receptionist.

### Phase 3: Hard-to-copy features (months 4–6)
- Bins-left-out computer vision, trained on Bin Caddie footage.
- A partner portal with referral tracking.
- Property-management-system integrations (Hostaway and Guesty partner applications).
- **Multi-tenant refactor:** each customer gets their own region, service type, data and branding.

---

## 6. Turning it into a product that sells for thousands

### Who it's for
The software isn't really "Bin Caddie software". It's a **lead engine for businesses that serve short-stay properties.** The same eight modules work for:

- STR cleaners
- linen services
- pool and garden contractors
- pest control
- handymen
- photographers
- co-host businesses
- management-rights operators

They also work in any region Inside Airbnb or council data covers: Gold Coast, Byron, Whitsundays, Mornington Peninsula and others. Bin Caddie becomes the first case study.

### What it does that a generic CRM can't
1. **An STR market map with route-fit scoring.** No generic CRM has this.
2. **A named list of the managers who control about 40% of listings,** refreshed automatically.
3. **Compliance built into the code** for Australian rules: the Spam Act, the Do Not Call Register, the Telemarketing Standard and the Privacy Act. This answers the buyer's fear of being fined.
4. **Field data capture** (Noosa signs, street signals), which competitors can't buy.
5. **Property-management-system integration,** which locks in the customers your customer wins.

### Pricing
These are suggestions anchored to Australian benchmarks: agencies charge $2,500–5,000 a month for outreach-only lead gen, hipages averages about $21 per lead, and US list tools such as PropStream cost US$99–699 a month.

| Package | Price (AUD) | Includes |
|---|---|---|
| **Done-for-you build (Bin Caddie tier)** | $3,500–7,500 setup + $750–1,500/month | The full engine configured for one business and region, plus a monthly campaign run and report |
| **SaaS seat** | $299–799/month per business per region | Self-serve map, account list, sequences, mail builder (resold through GoHighLevel's SaaS mode, with your custom modules) |
| **Regional exclusivity** | +$500–1,500/month | Only one bin, cleaning or linen business per region gets the account list. This scarcity is what makes it worth thousands. |
| **Performance option** | $150–250 per signed property, or $25–60 per qualified lead | For buyers who won't pay a retainer; you carry the risk |

**Selling Bin Caddie specifically:**

- Offer Phase 0 for a modest fee, or free in exchange for being the case study and testimonial.
- Then move to done-for-you pricing, with a performance kicker tied to signed properties.
- Their 2-week free trial and photo proof are already strong conversion assets; the engine feeds them.

---

## 7. Risks and how to handle them

| Risk | Mitigation |
|---|---|
| Inside Airbnb terms (housing-research mission, no republishing) | Use only for internal analysis and maps; never resell or show raw data; pull fresh per customer; get a legal opinion before scaling |
| Spam Act breach through over-broad email | Only published business addresses, with source logged; role relevance; low volume; suppression across all channels |
| Privacy Act applies to you as the vendor | Privacy policy, data minimisation (no private-person records), automated decision-making disclosure from 10 December 2026, deletion on request |
| Being seen as surveillance (street data) | Street data only chooses where to send mail; it is never mentioned to anyone; on-device blurring; short retention |
| Bin Caddie can't handle the volume | Route-fit scoring; release leads gradually based on capacity; manager pilots capped at 5 properties |
| Overlap with partner Turbo's Wheelie Clean | Agree a referral arrangement early; cleaning upsells go to them |
| Manager churn or consolidation | Property-management-system integration and monthly reports raise switching costs; diversify across tiers |
| Unverified Noosa bin rule | Check the current approval conditions before using that claim in any marketing |

---

## 8. Do these first, this week

1. **Download the Inside Airbnb Sunshine Coast dataset** and rank hosts by listing count. You'll have your Tier A list of about 87 names in an hour.
2. **Query Sunshine Coast Council's development-application API** for short-term accommodation applications since 2023, and list the addresses for "To the Owner" letters.
3. **Get the current Noosa short-stay approval conditions PDF** and confirm the bin and waste wording. If the rule exists, it's the strongest sales message available.
4. **Set up GoHighLevel and a separate cold-email domain** now, so the domain has warmed up by the time the list is ready.
5. **Confirm the Turbo's Wheelie Clean relationship terms with Bin Caddie** so the engine's cleaning upsell doesn't create channel conflict.
6. **Book a one-hour session with an Australian privacy or marketing lawyer** on Inside Airbnb use and Spam Act inferred consent. That legal sign-off is a selling point.

---

### Key sources
- Inside Airbnb, Sunshine Coast, 28 Sep 2026: data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/; data policies: insideairbnb.com/data-policies/
- Sunshine Coast Council DA open data: geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer
- Noosa short-stay letting: noosa.qld.gov.au/short-stay-letting
- Airbtics Sunshine Coast managers: airbtics.com/top-airbnb-management-companies-in-sunshine-coast-australia
- Airbnb Terms of Service s 11.1 (5 Feb 2026): airbnb.com.au/help/article/2908
- Do Not Call Register: donotcall.gov.au; Telemarketing Industry Standard 2017: legislation.gov.au/F2017L00323
- ACMA spam enforcement (e.g. Commonwealth Bank $7.5m, Oct 2024): acma.gov.au
- REIQ on Valuer-General data and marketing: reiq.com/articles/the-fine-line-between-marketing-and-privacy
- Titles Queensland searches: titlesqld.com.au/title-searches/
- The full research notes, with every citation, are in `research_notes/Bin Caddie lead generation plan/` (data_sources.md, compliance.md, tech_stack_pricing.md).
