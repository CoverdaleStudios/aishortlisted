# Data sources for identifying short-term rental (STR) properties, owners and managers on the Sunshine Coast and in Noosa (QLD), for Bin Caddie B2B lead generation

Research date: 10 October 2026. Every figure below is date-stamped where the source gives a date. "Verified" means I checked it directly against the primary source or dataset during this research, either by querying it live or by downloading it.

---

## Q0. Ranked inventory: which sources are most useful?

### Takeaway
No public register in either council names STR owners or managers. The most practical sources, in order:
1. **Inside Airbnb, Sunshine Coast dataset.** Free, verified 28 Sep 2026, 7,315 listings with host display names and host listing counts.
2. **Sunshine Coast Council's open DA feature service.** Free, CC BY. Its description field includes the address and applicant/owner names for STA approvals.
3. **The Airbtics "top management companies" page and the Airbnb Co-Host Network pages.** Free, and give named managers.
4. **Tourism Noosa / Visit Sunshine Coast directories and the Google Maps manager list.**
5. **Noosa's approval signs, which must be shown at the front of each approved property.** Each sign carries the approval number and the contact details. Collecting them is a manual drive-by job.
6. **Titles Queensland.** Use it for one-off title searches (A$25.71 + GST) and CMS searches (body corporate address) on high-value complexes only.

Valuer-General/QVAS owner-name data through brokers such as CoreLogic **cannot legally be used for direct marketing**: the Code of Conduct prohibits it.

### Cited findings: ranked table (details in the sections below)

| Rank | Source | Address? | Owner name? | Manager / contact? | Listing count / pro flag? | Access & cost | Update freq. | Marketing-use restriction |
|---|---|---|---|---|---|---|---|---|
| 1 | Inside Airbnb, Sunshine Coast (`data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/`) | No street address. Lat/long is jittered, plus suburb | Host display name only, e.g. "Cate" or a company name | Host display name = company for pros (e.g. "Welcome Ready Holiday Homes" 191 listings) | Yes: `host_listings_count`, `calculated_host_listings_count` | Free CSV download | Roughly quarterly; latest scrape 28 Sep 2026 | Licence is CC BY 4.0 per the download page. The Data Policies page says "Do not republish the data", asks users not to scrape the site, and says "Do good with the data" |
| 2 | Sunshine Coast Council DA layer (ArcGIS `PlanningCadastre/Applications_SCRC/MapServer`) and Development.i | Yes, street address in the description | Often yes, as applicant/owner names in the description | Planning consultant named | No | Free REST API / open data, CC BY 3.0 AU | Live; latest record received 27 Sep 2026 | CC BY. Personal names are still personal information, so contact must comply with the Spam Act / DNCR |
| 3 | Airbtics "Top Airbnb management companies – Sunshine Coast" | No | No | Yes, 46 named companies with counts | Yes | Free web page. Paid plans US$29–295/mo | Page updated June 2026 | Airbtics site terms not checked |
| 4 | Airbnb Co-Host Network pages (Noosa Heads, Sunshine Beach, Peregian Beach, Montville, etc.) | No | No | Co-host first name, location, rating, years hosting | No | Free, browse manually | Live | Airbnb ToS s.11.1 bans scraping and the use of members' personal information for commercial messages |
| 5 | Tourism Noosa (visitnoosa.com.au directory, 550+ members), Visit Sunshine Coast, Google Maps, REIQ | Business address | No | Yes, business contact | Some self-reported ("100+ properties") | Free, manual | Ongoing | Use published business contacts only. Spam Act conspicuous-publication rules apply |
| 6 | Noosa approval signs at the front of each approved property | Yes (physical) | Sometimes; the contact may be the owner | Yes, contact details and approval number on a sign with lettering of at least 50 mm | No | Field collection by driving/walking streets | N/A | Not a register. Ordinary privacy and Spam Act rules apply |
| 7 | Noosa Short Stay Snapshot (quarterly PDF) | No (suburb totals only) | No | No | Aggregate counts (3,167 approvals to June 2026) | Free PDF | Quarterly | N/A (aggregate) |
| 8 | Titles Queensland title search / CMS search | Yes (input) | Yes (registered owner) | CMS search returns the body corporate address, often the BCM's | No | A$25.71 + GST per current title search, through approved distributors (InfoTrack, Dye & Durham, etc.) | Live | Personal information. Best used per property, not for bulk marketing |
| 9 | Management rights brokers (ResortBrokers, etc.) | Suburb only; building name withheld | No | Broker | Not shown | Free web | Live | N/A |
| 10 | QVAS / Valuer-General data through CoreLogic, Pricefinder, APM, Equifax, onthehouse | Yes | Yes (name and service address) | No | No | Paid subscription | Weekly-ish | **Prohibited for direct marketing** under the Personal Identification Information in Property Data Code of Conduct |
| 11 | AirDNA / AirROI / PriceLabs Market Dashboard | Approximate | No evidence of owner names | Not verified | AirDNA/AirROI market counts | AirDNA: price not published (third-party estimate US$15–40/mo per market). PriceLabs: US$9.99/mo for up to 1,000 listings. AirROI API: from US$0.01/call | Daily–monthly | Vendor ToS |
| 12 | Sunshine Coast transitory accommodation rate category | No public list | No | No | ~6,000 properties (2023) | Not public. Rates records are confidential | Six-monthly | Not available |

Sources for each row are cited in the sections below.

### Inferences
- The best-value workflow combines four steps:
  1. Take the free Inside Airbnb CSV and rank hosts by `calculated_host_listings_count`. 87 hosts have 10 or more listings and together control 2,911 listings.
  2. Cross-reference those hosts with Airbtics, Tourism Noosa and Google Maps to get business contact details.
  3. Sell to the roughly 100–200 professional managers first. They are B2B buyers with many bins each.
  4. Use the SCC DA layer and Noosa signage to reach individual owners and complexes.

---

## Q1. Does Noosa Council have a PUBLIC short-stay register, and what does it show?

### Takeaway
No. Noosa issues approvals under the "Short Stay Letting and Home Hosted Accommodation Local Law", in force since February 2022, and publishes only an aggregate quarterly "Short Stay Snapshot" PDF. I found no searchable or downloadable property-level register with addresses, approval holders or contact persons. However, every approved property must display a sign at the front showing the approval number and the current contact details, which makes field collection possible.

### Cited findings
- **Law and approvals:** The local law has been in place since February 2022. Approval is one-off and must be renewed annually while short stay letting continues. — [Noosa Council, Short Stay Letting](https://www.noosa.qld.gov.au/short-stay-letting)
- **Application fees, 2026/27:**
  - House: A$1,748
  - House used as principal place of residence: A$329
  - Unit: A$455
  - Managed complex: A$450
  - Home hosted: A$329
  - Change or transfer: A$273

  — [Noosa Council](https://www.noosa.qld.gov.au/short-stay-letting)
- **Annual renewal fees from 1 July 2026:**
  - House: A$800
  - House used as principal place of residence: A$200
  - Unit: A$300
  - Unit used as principal place of residence: A$150
  - Home hosted: A$200
  - Managed complex: A$75
  - Managed complex used as principal place of residence: A$50

  — [Noosa Council](https://www.noosa.qld.gov.au/short-stay-letting)
- **Exemptions:** Visitor-accommodation-only sites and the Hastings Street Mixed Use precinct under Noosa Plan 2020 are exempt, as are motels, hotels and backpackers. Many resort complexes in Hastings Street therefore hold **no** local-law approval. — [Noosa Council](https://www.noosa.qld.gov.au/short-stay-letting)
- **No register on the main pages:** The main short-stay page mentions no public register, address search or contact lookup. The only public numbers are the 24/7 hotline, (07) 5329 6466, and general enquiries, (07) 5329 6500. — [Noosa Council](https://www.noosa.qld.gov.au/short-stay-letting); [Short Stay Snapshots page](https://www.noosa.qld.gov.au/Planning-and-Development/Short-stay-letting-and-home-hosted-accommodation-local-law/Short-stay-letting/Short-Stay-Snapshots)
- **Snapshot contents:** The snapshot was launched on 21 Feb 2024 and is updated quarterly. It shows current approval numbers, compliance notices and fines, refusals, suburbs with the most approvals, and hotline calls. It does not list individual properties. — [Noosa Council media release 2024](https://www.noosa.qld.gov.au/About-Council/News-and-publications/Media-releases/2024/Short-Stay-Letting-snapshot-provides-additional-transparency); [Sunshine Coast News, 25 Feb 2024](https://sunshinecoastnews.com.au/2024/02/25/petition-says-short-stay-law-stumbling-as-platform-launched)
- **Latest snapshot (Feb 2022 – June 2026), read with WebFetch's PDF extraction:**
  - Total current approvals: 3,167
  - By type:
    - Duplex/multiple dwelling: 2,438
    - Dwelling (other): 452
    - Dwelling as principal place of residence (limited to 60 days, 4 times a year): 153
    - Home hosted dwelling: 75
    - Home hosted studio/cabin: 28
    - Duplex as principal place of residence: 21
  - Top suburbs:
    - Noosa Heads: 1,163
    - Noosaville: 1,022
    - Sunshine Beach: 442
    - Peregian Beach: 217
    - Sunrise Beach: 142
    - Tewantin: 32
    - Noosa North Shore: 28
  - Infringements: 185

  — [Noosa Short Stay Snapshot Feb 2022–June 2026 (PDF)](https://www.noosa.qld.gov.au/files/assets/public/v/2/planning-and-development/documents/short-stay/short-stay-snapshot-feb-2022-june-2026-correct.pdf)
- **Earlier figures, which conflict:** In February 2024, 2,599 approvals were reported, with Noosa Heads at 950, Noosaville at 864 and **Sunshine Beach at 839**. — [Sunshine Coast News](https://sunshinecoastnews.com.au/2024/02/25/petition-says-short-stay-law-stumbling-as-platform-launched). The June 2026 extraction shows Sunshine Beach at 442. That may reflect extraction error or a re-classification (for example, Sunrise Beach split out), so verify against the PDF visually.
- **Contact person:** A contact person must be identified for each premises at all times. It may be an individual, letting agent, property manager or security firm. The contact must be available 24/7, live or work within a 20 km radius, and respond to complaints within 30 minutes. — [Noosa conditions of approval](https://noosa.qld.gov.au/downloads/file/4312/conditions-of-approval-short-stay-letting); [Noosa guide to good management](https://noosa.qld.gov.au/downloads/file/3252/guide-to-good-management-of-ssl-and-hha). These are as summarised by search, because the PDF did not render via fetch.
- **Approval notice sign:** An approval notice must be displayed at the front of the property, or where body corporate by-laws require. It must show the approval number and current contact details in lettering at least 50 mm high. — [Noosa complaints process](https://www.noosa.qld.gov.au/Planning-and-Development/Short-stay-letting-and-home-hosted-accommodation-local-law/Short-stay-complaints-process); [Noosa conditions of approval](https://noosa.qld.gov.au/downloads/file/4312/conditions-of-approval-short-stay-letting)
- **Bin conditions in the 2021 draft:** The draft conditions required waste containers to be kept clean, put kerbside for collection, and not left kerbside more than 24 hours before or after collection day. I could not confirm that this wording survives in the current conditions. — [Noosa Planning & Environment Committee agenda, 9 Mar 2021](https://noosa.qld.gov.au/downloads/file/2763/2021-03-09-planning-environment-committee-meeting-agenda); [General committee minutes, 15 Mar 2021](https://noosa.qld.gov.au/downloads/file/2781/2021-03-15-general-committee-minutes)
- **Online application tracking:** Noosa's Application Tracking (T1Cloud eTrack) covers development applications "from lodgement to determination". It is not described as covering local-law approvals. — [Noosa Planning Online](https://www.noosa.qld.gov.au/Planning-and-Development/Development-tools-and-guidelines/Planning-online)
- **No DA open data:** Noosa publishes open data on data.gov.au under CC BY 4.0, but I found no development application dataset there. — [Noosa Open data](https://www.noosa.qld.gov.au/Community/Mapping/Open-data)

### Inferences
- **Bin rules as a selling point:** Bin compliance is likely a condition of Noosa approvals, since waste was one of the amenity problems the law targets. A bin put-out service lets Noosa operators and their contact persons meet the "not more than 24 hours" kerbside rule and avoid complaints, compliance notices and fines (185 infringements to date). This should be verified against the current conditions PDF before it is used in marketing.
- **The contact person is the real buyer:** Most approvals (2,438) are duplex or multiple dwelling units, mainly in Noosa Heads and Noosaville. The person on the sign must respond within 30 minutes and live within 20 km. That person is very often a local letting agent, making them the natural B2B buyer.
- **Signs are a ground-truth source:** A street survey of signs in Noosa Heads, Noosaville, Sunshine Beach and Peregian would yield approval numbers and manager names and phone numbers.

### Gaps
- I could not confirm whether Noosa would release the approval list, including addresses and contact persons, under a Right to Information application. That is likely to be refused or redacted for personal information, but I found no source either way.
- The current conditions-of-approval PDF did not render. The final bin and waste wording is therefore unverified.
- I could not reach the Noosa eTrack tool (it timed out), so I could not check whether short-stay approvals appear there.

---

## Q2. Sunshine Coast Council: is there STA registration, a rating category, or searchable development approvals?

### Takeaway
Sunshine Coast Council has **no STA registration or permit local law**. It regulates through:
- **a differential "Transitory Accommodation" rate category.** This is non-public and covered roughly 6,000 properties in 2023.
- **the Planning Scheme 2014.** Some dwellings built after 2014 in low-density zones need a material change of use (MCU) approval for STA.

The best SCC data source is the council's open ArcGIS DA service, which has a free REST API under CC BY 3.0 AU. Its `description` field contains the street address, use type and applicant/owner names. There are 292 decided and 22 in-progress applications mentioning "short-term accommodation", plus 690 dual occupancy and 186 secondary dwelling applications since 2023. The data is live to 27 Sep 2026.

### Cited findings
- **Transitory accommodation categories:** The differential general rate categories for "Transitory Accommodation – non-domiciled property" are 16T, 17T, 18T, 19T, 27T and 29T, as defined in Section 3.4, Table 1 of the 2026–27 Revenue Statement. Owners can object if they used the property themselves for at least 28 days in a six-month period. — [SCC Rates information](https://www.sunshinecoast.qld.gov.au/pay-and-apply/rates/rates-information)
- **Scale and rate impact:** In August 2023, "almost 6000" short-term holiday rental properties faced rate rises. Examples were low-rise units rising from A$1,896 to A$2,813, and houses from A$2,087 to A$2,813. — [Sunshine Coast News, 2 Aug 2023](https://sunshinecoastnews.com.au/2023/08/02/rates-rise-row-short-stay-accommodation-owners-face-hike)
- **No STA permit on the business licensing page:** SCC's "Tourism and accommodation" licensing page covers only caravan parks and camping (Local Law No. 1, 2011) and rural cabins (MCU required). It has no holiday-letting permit and no register. — [SCC Tourism and accommodation](https://www.sunshinecoast.qld.gov.au/business/supporting-your-business/permits-and-licences/tourism-and-accommodation)
- **2021 plans:** SCC planned a short-stay local law with a hotline, and fees "subject to Council's budget process". I found no evidence that a registration scheme commenced. — [Sunshine Coast News, 20 Oct 2021](https://sunshinecoastnews.com.au/2021/10/20/short-stay-letting-law)
- **Planning approvals:** Under Planning Scheme 2014, properties built after 2014 in low-density zones may need an MCU or DA to operate STA. Pre-2014 dwellings generally do not. — [Real Estate Business, 31 Jan 2023](https://www.realestatebusiness.com.au/property-management/25055-a-2nd-qld-council-is-cracking-down-on-unapproved-airbnbs)
- **TLPI 01/2025:** This instrument affects the planning scheme for resort complexes and short-term accommodation where the use is an accommodation hotel. It targets hotels and resorts, not houses. — [SCC public notice TLPI 01/2025](https://www.sunshinecoast.qld.gov.au/council/public-notices/tlpi-01-2025-accommodation-hotel-incentive-measures)
- **Development.i:** It covers all DAs since 2007 and needs no login to search. It has no keyword search and is searched by address, suburb, application number or map. Documents are published for MCU and similar applications. — [SCC Development.i](https://www.sunshinecoast.qld.gov.au/development/development-tools-and-guidelines/development-i/); [Development.i FAQ](https://www.sunshinecoast.qld.gov.au/development/development-tools-and-guidelines/development-i/development-i-freqaskques/using-the-system)
- **Open data feature service (verified by live query on 10 Oct 2026):**
  - Endpoint: `https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer`
  - Layers: DAs in progress (0), decided/past (1), building, plumbing, and "approvals varying the effect of a planning scheme"
  - Fields: decision, progress, assessment_level, category_desc, d_decision_made, **description**, d_date_rec, plus geometry
  - Licence: CC BY 3.0 AU
  - Hub listing: [SCC open data – Applications DevI SCRC](https://data.sunshinecoast.qld.gov.au/datasets/scrcpublic::applications-devi-scrc?layer=1)
- **Query results (verified 10 Oct 2026):**
  - Description LIKE "%SHORT%TERM%ACCOMM%": 292 decided/past and 22 in progress; 144 received since 1 Jan 2023
  - Since 2023: 690 dual occupancy, 186 secondary dwelling, 16 tourist park, 7 resort complex, and 14 nature-based tourism applications
  - Latest record received: 27 Sep 2026

  — [SCC ArcGIS service](https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer)
- **Example descriptions (verified), showing that owner names are exposed:**
  - "59 Ayrshire Rd YANDINA – Short-Term Accommodation – Simone Ann Octavia Burke – URBN Town Planning"
  - "First Bay By Mosaic 242 and 253/131 Coolum Tce COOLUM BEACH – Short Term Accommodation (2 units) – [owner names] – Adapt Development Management Pty Ltd"
  - "Lot 41 & 42 Green Turtle Place MARCOOLA – … Short-Term Accommodation (68 Dwellings) … – Rochedale Enterprises Pty Ltd & Turtle Sands Marcoola Pty Ltd"

  — [SCC ArcGIS service](https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer)

### Inferences
- **The DA layer is the only free, bulk, address-plus-name STA source in either LGA.** It captures only properties that needed an approval: hinterland cabins, post-2014 dwellings, and new complexes. That is probably a few hundred, a small fraction of the roughly 6,000 rated as transitory.
- **Complexes are where the volume is.** New mixed-use and STA complexes such as Turtle Sands Marcoola (68 dwellings) are high-value targets for bin-room management, and they show up in this layer.
- **Dual occupancy and secondary dwelling DAs are a weak, indirect signal.** Many are long-term rentals or family use.

### Gaps
- I could not find SCC's 2026–27 Revenue Statement definition of "transitory accommodation" or the method SCC uses to identify such properties. It may use platform data or owner declarations.
- I found no evidence of a 2024–2026 SCC STA local law or registration scheme. A third-party blog (rakidzich.com) claims a "registration" framework, but this is uncorroborated by council pages and should be treated as unreliable.
- SCC's proposed new planning scheme has a "Short-term accommodation" information sheet ([haveyoursay information sheets](https://haveyoursay.sunshinecoast.qld.gov.au/newplanningscheme/information-sheets)), but I did not review its content.

---

## Q3. Queensland state level: an STR register, body corporate (BCCM) records, Titles Queensland, and Valuer-General owner data

### Takeaway
- **STR register:** Queensland has no statewide STR register as of October 2026. The government only "committed to looking into" one after the 2023 UQ review.
- **Titles Queensland:** A current title search costs A$25.71 + GST and reveals the registered owner. A CMS search through resellers such as Landchecker returns the scheme name and **body corporate address**, often the body corporate manager's address.
- **Valuer-General data:** QVAS data, including owner names, is sold through brokers such as CoreLogic, but the Code of Conduct **prohibits use for direct marketing**.

### Cited findings
- **2023 UQ review:** It found about 19,773 active STRs in Queensland in Q1 2023, of which about 11,193 were used on a permanent basis. Prevalence was highest in Noosa and the Sunshine Coast. The government committed "to looking into the implementation of a short-term rental registration system" and to consult the industry reference group and LGAQ. — [Inside Local Government, 3 Aug 2023](https://insidelocalgovernment.com.au/queensland-housing-review-reveals-limited-impact-of-short-term-rentals/)
- **Status in December 2024:** A parliamentary answer notes that LGAQ called for a statewide registration and data system. I found no later implementation. — [Qld Parliament QoN 1135-2024](https://documents.parliament.qld.gov.au/tableOffice/questionsAnswers/2024/1135-2024.pdf)
- **Titles Queensland fees (FY26/27, excl. GST):**
  - Current title search: A$25.71
  - Historical title search: A$37.88
  - Survey plan image: A$27.56
  - Dealing image: A$50.16
  - Orders go through approved distributors: Confirm, Creditworks, Dye & Durham, Equifax, InfoTrack, PSI Global and Fynd.

  — [Titles Queensland – title searches](https://www.titlesqld.com.au/title-searches/)
- **CMS number:** It appears on the title search. A QLD CMS search returns the scheme name, body corporate address, CMS, dealing number, regulation module and linked titles and plans. It is delivered within 2 hours in business hours, with the price shown at checkout. — [Landchecker help](https://help.landchecker.com.au/en/articles/12888823-how-to-conduct-a-qld-community-title-scheme-statement-search)
- **No contact details from the Commissioner:** The Office of the Commissioner for Body Corporate and Community Management does not hold body corporate contact details. It refers enquirers to Titles Queensland or the body corporate's records. Body corporate managers do not need a Queensland licence. — [Qld Govt – Ask a body corporate question](https://www.qld.gov.au/bodycorporatequestion); [Body corporate managers under other Acts](https://www.qld.gov.au/housing/body-corporate/roles/body-corporate-managers-under-other-acts)
- **Valuer-General products:** These include abbreviated and full sale searches, which "including vendor and purchaser names". They are bought through Valuer-General business centres or participating QVAS brokers. — [Qld Govt – Property sales and valuation products](https://www.qld.gov.au/environment/land/title/property-sales-maps-and-reports)
- **Valuation roll:** It includes owners' names and addresses, and the Valuer-General can suppress these for safety reasons. — [Qld Govt – About land valuations (privacy)](https://qld.gov.au/environment/land/title/valuation/privacy)
- **Broker data and the marketing ban:** Licensed brokers (CoreLogic RP Data, onthehouse, APM, PriceFinder, Equifax) sell QVAS data that includes "the owner's name and service address". "The Personal Identification Information in Property Data Code of Conduct prohibits the use of this data for direct marketing." The Office of Fair Trading received 22 complaints in 2016–17, of which 6 were substantiated. — [REIQ / Office of Fair Trading, 25 Nov 2019](https://www.reiq.com/articles/the-fine-line-between-marketing-and-privacy)

### Inferences
- **Use title searches selectively.** At about A$28 incl. GST each, title searches suit a few dozen high-value complexes, to identify the owner or developer entity and, through the CMS, the body corporate manager. They are uneconomic for thousands of houses.
- **Do not use CoreLogic/RP Data owner names for mail-outs or calls.** Using owner-name data from those brokers for Bin Caddie marketing would breach the Code. That data is still usable for internal market sizing only.

### Gaps
- The exact Titles Queensland or reseller price for a CMS search was not shown on the pages checked.
- I did not confirm whether Titles Queensland offers search by owner name, or under what restrictions.
- I did not confirm the current (2026) wording of the QVAS licence and the Code of Conduct.

---

## Q4. Listing-level data: Inside Airbnb, AirDNA, AirROI, PriceLabs, Airbtics, Key Data

### Takeaway
**Inside Airbnb covers "Sunshine Coast, Queensland", including Noosa.** The latest scrape is 28 Sep 2026, with 7,315 listings. It is free and includes host display names and host listing counts, which makes it the single best tool for separating professional managers from individual owners. Commercial tools (AirDNA, AirROI, PriceLabs, Airbtics) mainly give market metrics. Of these, only Airbtics publishes named management-company rankings.

### Cited findings
- **Coverage:** Inside Airbnb's Australian regions include `qld/sunshine-coast/2026-09-28` and Brisbane. There is no separate Noosa or Gold Coast dataset. — [Inside Airbnb – Get the data](https://insideairbnb.com/get-the-data/)
- **Licence and use policy:**
  - Licence: "Creative Commons Attribution 4.0 International License". — [Inside Airbnb – Get the data](https://insideairbnb.com/get-the-data/)
  - The Data Policies page says "Do not republish the data", asks users not to scrape the site, and says free data covers the last 12 months while archived data needs a request.
  - The project's mission is about the housing impact of STRs, and the page says "Do good with the data".

  — [Inside Airbnb – Data policies](https://insideairbnb.com/data-policies/)
- **My analysis of `listings.csv.gz` (scraped 28 Sep 2026; downloaded and analysed 10 Oct 2026):**
  - Size: 7,315 listings; 6,832 entire homes/apartments; 5,381 with at least one review in the last 12 months
  - Hosts: 3,195 unique. 2,509 have 1 listing, 502 have 2–4, 97 have 5–9, and 87 have 10 or more. The 87 large hosts control 2,911 listings, about 40% of the total.
  - Fields include: `host_id`, `host_name`, `host_url`, `host_since`, `host_location`, `host_about`, `host_is_superhost`, `host_listings_count`, `host_total_listings_count`, `calculated_host_listings_count`, `latitude`/`longitude`, `neighbourhood_cleansed`, `property_type`, `bedrooms`, `price`, `estimated_occupancy_l365d`, `estimated_revenue_l365d`, `license`, `listing_url`
  - **`license` is empty for all 7,315 listings**
  - Top suburbs: Noosa Heads 975, Mooloolaba–Alexandra Headland 821, Noosaville 549, Maroochydore–Kuluin 542, Coolum Beach 499, Sunshine Beach 496, Caloundra–Kings Beach 490

  — [Inside Airbnb Sunshine Coast listings.csv.gz](https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/data/listings.csv.gz)
- **Largest hosts by listing count (Inside Airbnb, 28 Sep 2026):**

  | Host name | Listings |
  |---|---|
  | Welcome Ready Holiday Homes | 191 |
  | Caloundra Holiday Centre | 128 |
  | Team Tabi | 116 |
  | Niche Holidays Noosa | 112 |
  | "Cate" | 110 |
  | Holiday Caloundra | 92 |
  | Aspire Property Management | 91 |
  | Accom Caloundra | 89 |
  | G1 Holidays | 82 |
  | SunnyBNB | 82 |
  | Belle Escapes Coolum Noosa Marcoola | 81 |
  | Sunshine Beach Real Estate | 60 |
  | Holiday Mooloolaba | 59 |
  | Noosa Holiday Rentals | 53 |
  | Laguna Holidays | 52 |
  | Holiday Homes @ Noosa | 50 |
  | Noosa Beach Abodes | 46 |
  | Accom Noosa | 39 |
  | Green Hill Accommodation Management | 39 |
  | Zinc Properties Noosa | 31 |
  | The Rise Noosa | 28 |
  | Host Angel Noosa | 25 |
  | Prestige Holiday Homes | 24 |
  | Layne Property Management | 23 |
  | Number One Hastings | 23 |
  | Flair Property Group | 20 |

  — [Inside Airbnb Sunshine Coast listings](https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/data/listings.csv.gz)
- **Neighbourhood grouping caveat:** The neighbourhood file groups areas into "Noosa" (2,419 listings) and "Sunshine Coast" (4,896). The "Noosa" group includes Coolum Beach, Peregian Springs and Eumundi–Yandina, which are in the Sunshine Coast LGA, so the grouping does not match council boundaries. — [Inside Airbnb neighbourhoods.csv](https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/visualisations/neighbourhoods.csv)
- **AirDNA:**
  - Reports 5,863 active STR listings for "Sunshine Coast" as of August 2026, across Airbnb, Vrbo and Booking.com, with active supply down 42.2% year on year. This is a search-snippet figure. — [AirDNA Sunshine Coast supply](https://www.airdna.co/vacation-rental-data/app/au/queensland/sunshine-coast/supply)
  - Paid pricing is not published. One third-party review estimates US$15–40/month per market; another says paid-tier amounts are not listed. — [bnbcalc AirDNA review 2026](https://www.bnbcalc.com/reviews/airdna-review-2026); [strspecialist AirDNA review](https://strspecialist.com/reviews/airdna-analytics-review)
- **AirROI:**
  - Free web analytics; its API costs from US$0.01 per call (vendor's own claim). — [AirROI blog](https://www.airroi.com/blog/best-airbnb-scrapers); [AirROI llms.txt](https://airroi.com/llms.txt)
  - Its Sunshine Coast page showed only 44 active listings, which conflicts strongly with AirDNA and Inside Airbnb and suggests a narrow geographic definition. — [AirROI Sunshine Coast](https://airroi.com/airbnb-data/australia/queensland/sunshine-coast)
- **PriceLabs Market Dashboard:**
  - Price per dashboard per month (plus tax): US$9.99 for up to 1,000 listings, US$19.99 for up to 5,000, US$39.99 for up to 10,000, US$79.99 for up to 20,000
  - Refreshes daily; month-to-month billing

  — [PriceLabs billing help](https://help.pricelabs.co/portal/en/kb/articles/market-dashboard-billing-and-subscription)
- **Airbtics:**
  - Publishes a free "Top Airbnb Management Companies in Sunshine Coast" page (updated June 2026) with 46 named companies and their active-listing counts. The top entries are Melanie And Verena 165, Niche Holidays Noosa 113, Team Tabi 102, Sunny Bnb 92, Aspire 91, Belle Property Escapes 87, Accom Caloundra 85 and Utopia Rentals 84; MadeComfy has 33.
  - Active means listed for more than 90 days with at least one booking in the last 12 months. — [Airbtics Sunshine Coast managers](https://airbtics.com/top-airbnb-management-companies-in-sunshine-coast-australia)
  - Paid plans: Expert US$29/mo and Scale US$295/mo, according to the current page; older pages show different prices. — [Airbtics pricing](https://airbtics.com/pricing/)

### Inferences
- **Inside Airbnb beats the paid tools for this purpose.** Its host listing counts make it straightforward to rank professional managers, and the paid tools add little for identifying them.
- **The managers are a short list.** Roughly 87 hosts with 10 or more listings, plus about 97 with 5–9, form the core B2B prospect list. These ~184 hosts control about 3,500 listings.
- **"Cate", "Michelle" and similar first-name hosts with 50–110 listings** are almost certainly agency staff profiles. Click through `host_url` to see the company name in the profile bio.
- **Supply estimates differ widely** (AirDNA ~5,863 active vs Inside Airbnb 7,315 total). Inside Airbnb's count includes inactive listings, so use its 12-month-review count (5,381) as the active proxy.

### Gaps
- I did not research the Key Data Dashboard (keydatadashboard.com). Its data comes from property-management software and is generally aggregated with no host identities, but this is unverified.
- I did not verify whether AirDNA or AirROI expose host names or host IDs in exports or APIs.
- Inside Airbnb coordinates are deliberately anonymised (jittered) and include no street addresses, so properties need matching by photo or listing to get an address.

---

## Q5. What host information is publicly visible on Airbnb, Stayz and Booking.com, and what do their terms say?

### Takeaway
Airbnb shows the host's preferred first name **or business name**, years hosting, rating, reviews, Superhost status and a link to their other listings. Co-Host Network profiles are public and show the co-host's name, suburb, rating and years hosting. Airbnb's Terms (s.11.1, updated 5 Feb 2026) ban scraping and using members' personal information to send commercial messages, so Bin Caddie cannot cold-message hosts through Airbnb.

### Cited findings
- **Host profiles:** The host profile shows the preferred first name or business name, falling back to the legal first name. It can also show years hosting, average rating, identity-verification date, reviews and Superhost status. Co-Host Network profiles default to the first and last name and are "publicly available". — [Airbnb Help 3811](https://www.airbnb.com/help/article/3811); [Airbnb Help 3812](https://www.airbnb.com/help/article/3812)
- **Terms of Service, Australia (last updated 5 Feb 2026), s.11.1:**
  - "Do not use bots, crawlers, scrapers, or other automated means to access or collect data"
  - "Do not use the Airbnb Platform, our messaging tools, or Members' personal information to send commercial messages" (unless the recipient has given express consent)

  — [Airbnb Terms of Service (AU)](https://www.airbnb.com.au/help/article/2908)
- **Co-Host Network:** It launched in October 2024 in 10 countries, including Australia. — [eCommerceNews AU](https://ecommercenews.com.au/story/airbnb-launches-co-host-network-to-simplify-management)
  - Local pages exist for Noosa Heads, Sunshine Beach, Peregian Beach, Montville and Mount Mellum.
  - The Noosa Heads page (fetched 10 Oct 2026) shows co-hosts "Joe & Brooke" (4.84 rating, 6 years), "Craig" (4.91, 3 years) and "Ruby" (Sunshine Beach, 4.90, 11 years).
  - Cards show name, location, bio, rating and years hosting. They do not show a business name or listing count.

  — [Airbnb Noosa Heads Co-Host Network](https://www.airbnb.com.au/host/noosa-heads-australia/co-hosts); [Sunshine Beach Co-Host Network](https://airbnb.com/host/sunshine-beach-australia/co-hosts)
- **Cross-check against Inside Airbnb:** "Joe & Brooke" also appear in Inside Airbnb with 22 listings. — [Inside Airbnb listings](https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/data/listings.csv.gz)
- **Stayz:** Stayz is a Vrbo affiliate, with listings shared across the Vrbo network. — [Rentals United – Stayz](https://rentalsunited.com/vacation-rental-services/stayz/)

### Inferences
- **Use Airbnb to identify, not to contact.** Manual browsing to identify a manager's business name is fine. Contact should then happen off-platform, through the manager's own published business email or phone, under Spam Act inferred-consent rules (see Q9).
- **The Co-Host Network pages are a free, curated list** of local professional and semi-professional managers in Noosa and Sunshine Beach.

### Gaps
- I did not verify Stayz/Vrbo and Booking.com host-profile fields or their scraping clauses. Both are generally understood to prohibit scraping, but this is not verified here.
- I did not verify whether Airbnb listings in Australia display co-host names on the listing page.

---

## Q6. Professional holiday-letting managers in Sunshine Coast and Noosa: how to compile a list, and how many there are

### Takeaway
Compile the list from:
- Inside Airbnb host counts
- Airbtics' named ranking (46 companies)
- the Tourism Noosa member directory (550+ members, with individual holiday-letting agency pages)
- Visit Sunshine Coast
- the Airbnb Co-Host Network pages
- Google Maps searches such as "holiday letting Noosaville"

A realistic universe is about 150–200 managing entities. Roughly 85–90 of them manage 10 or more Airbnb listings.

### Cited findings
- **Inside Airbnb counts:** 87 hosts with 10 or more listings and 97 with 5–9 (Sep 2026). — [Inside Airbnb](https://data.insideairbnb.com/australia/qld/sunshine-coast/2026-09-28/data/listings.csv.gz)
- **Airbtics:** 46 named management companies on the Sunshine Coast (June 2026). — [Airbtics](https://airbtics.com/top-airbnb-management-companies-in-sunshine-coast-australia)
- **Tourism Noosa:** It has over 550 members across accommodation, tours, real estate agents and services. Directory pages exist for holiday-letting agencies including CAN Properties Noosa, Accom Noosa ("100+ properties"), Laguna Real Estate Holiday Rentals (since 1977) and Holiday Noosa / Utopia Rentals. — [About Tourism Noosa](https://www.visitnoosa.com.au/members/about-tourism-noosa); [Accom Noosa listing](https://visitnoosa.com.au/trade/directory/accom-noosa); [CAN Properties](https://visitnoosa.com.au/directory/can-properties-noosa); [Laguna](https://visitnoosa.com.au/directory/laguna-real-estate-holiday-rentals); [Utopia Rentals](https://visitnoosa.com.au/directory/holiday-noosa-accommodation-utopia-rentals)
- **Visit Sunshine Coast:** It has an accommodation directory, for example "Accommodation in Noosa". — [Visit Sunshine Coast](https://www.visitsunshinecoast.com/genservice/69016ed2dec0828563239a5d/accommodation-in-noosa)

### Inferences
- **Agencies and on-site managers are separate groups.** Many Inside Airbnb "hosts" with 20–60 listings are real-estate agency holiday-letting departments (e.g. Sunshine Beach Real Estate, Laguna, Flair Property Group). Resort on-site managers (e.g. Number One Hastings, The Rise Noosa, Caloundra Holiday Centre) are the other group. Each needs a different pitch:
  - **Agencies:** a portfolio-wide put-out and clean service
  - **On-site managers:** bin-room and communal bin cleaning

### Gaps
- I did not check the REIQ "find an agent" directory or its terms.
- I did not verify that national operators such as Hometime, MadeComfy and Airhost are active locally, apart from MadeComfy appearing in Airbtics with 33 listings.

---

## Q7. Strata and body corporate managers, and how to enumerate complexes

### Takeaway
SCA Queensland, with more than 1,200 individual and business members, runs a public member directory at directory.strata.community. The Queensland Government holds no body corporate contact register. To identify the manager of a specific complex, use a Titles Queensland CMS search, which gives the body corporate address and is often the body corporate manager's.

### Cited findings
- **SCA Qld directory:** SCA Qld represents more than 1,200 individuals and businesses, and its member directory is at directory.strata.community. — [SCA Qld About](https://www.qld.strata.community/qld-about-us)
  - The directory has categories (Strata Management, Maintenance, etc.) and browse-by-location. The Sunshine Coast was not visible on the first page.
  - Terms of use are linked but were not reviewed.

  — [SCA directory](https://directory.strata.community/)
- **No government contact register:** The Commissioner's office holds no body corporate contact details. — [Qld Govt](https://www.qld.gov.au/bodycorporatequestion)
- **CMS search contents:** The scheme name and body corporate address. — [Landchecker](https://help.landchecker.com.au/en/articles/12888823-how-to-conduct-a-qld-community-title-scheme-statement-search)

### Inferences
- **To enumerate complexes:**
  1. Cluster Inside Airbnb listings by approximate coordinates and listing names, which often name the building (e.g. "First Bay", "Oceans Mooloolaba").
  2. Add the SCC DA layer (multiple-dwelling and STA complexes).
  3. Add Booking.com/Wotif hotel-style apartment listings.
  4. Then use CMS searches on the top complexes.

### Gaps
- I did not enumerate Sunshine Coast strata managers. Firms named in the brief (Archers, PICA/Body Corporate Services, BCsystems) were not verified for local office presence.
- I found no count of community titles schemes in Sunshine Coast or Noosa.

---

## Q8. Resort and holiday-apartment buildings with on-site managers (management rights)

### Takeaway
Management-rights brokers list businesses by suburb only. ResortBrokers' Noosa page (10 Oct 2026) showed 9 records (3 available, 6 sold) with reference number, suburb and price, but **no building names or unit counts**. Broker news releases do name sold buildings. On-site managers are best identified directly from Inside Airbnb, Booking.com and Tourism Noosa.

### Cited findings
- **ResortBrokers Noosa page:**
  - 9 records, including available listings at Noosaville (net A$212,977, business only) and Noosa North Shore (net A$518,582)
  - Fields shown: reference, type, suburb and net price
  - Building names are not disclosed

  — [ResortBrokers Noosa](https://www.resortbrokers.com.au/management-rights-for-sale/queensland/noosa/)
- **Sales named in broker press releases:**
  - Oceans Mooloolaba Beach: A$11.2M, a Sunshine Coast record (2023)
  - On the Beach, Noosa: A$8.06M (Feb 2022)
  - Noosa Crest: 39 apartments, 30 in the letting pool (2024)

  — [ResortBrokers record sale](https://www.resortbrokers.com.au/learn/blog/media/resortbrokers-sets-record-sale.html); [Noosa Crest sale](https://www.resortbrokers.com.au/learn/blog/media/victorian-buyers-snap-up-noosa-crest-management-rights-through-resortbrokers.html)
- **ARAMA:** ARAMA (formerly QRAMA, formed 1991) had about 900 members in 2014. I did not find a public member directory. — [ResortBrokers blog on ARAMA](https://test.resortbrokers.com.au/learn/blog/arama-a-lot-more-than-just-a-social-club.html)

### Inferences
- **Resort managers are a dense target in Noosa.** Many Hastings Street resorts are exempt from Noosa's local law and so do not appear in council approvals. Inside Airbnb names some resort managers directly (e.g. "Number One Hastings", "The Rise Noosa", "Caloundra Holiday Centre"). A building-by-building visit or call list of the roughly 50–100 resort complexes in Noosa Heads, Noosaville, Mooloolaba and Caloundra is the efficient route.

### Gaps
- I found no count of management-rights complexes in either LGA.
- The ARAMA directory and the onsite-manager listings on theonsitemanager.com.au were not reviewed.

---

## Q9. Other signals, and the legal limits on using the data for marketing

### Takeaway
- **DAs:** Dual occupancy and secondary dwelling DAs are freely queryable through the SCC open data API (690 and 186 since 2023), but they are weak STR signals.
- **Sale listings:** Property sale listings that mention "holiday letting" or "Airbnb income" were not researched.
- **Legal limits:** Owner data from CoreLogic, RP Data or QVAS cannot be used for direct marketing. Email marketing to managers relies on Spam Act "conspicuous publication" inferred consent: a published business email, a message relevant to the recipient's role, and no "no-spam" statement.

### Cited findings
- **SCC open data counts since 2023:** 690 dual occupancy, 186 secondary dwelling, 16 tourist park, 7 resort complex and 14 nature-based tourism applications. — [SCC ArcGIS service](https://geopublic.scc.qld.gov.au/arcgis/rest/services/PlanningCadastre/Applications_SCRC/MapServer)
- **QVAS owner data:** The Code of Conduct prohibits direct-marketing use. — [REIQ/OFT](https://www.reiq.com/articles/the-fine-line-between-marketing-and-privacy)
- **Spam Act conspicuous publication:** Consent can be inferred only if the address is conspicuously published, there is no statement that commercial messages are unwanted, and the message relates directly to the recipient's role. Publication alone is not enough (Clarity1 case). — [Mondaq – Spamming and the Spam Act](https://www.mondaq.com/australia/consumer-law/996226/spamming-and-the-spam-act); [Osgoode – Clarity1](https://yorku.ca/osgoode/thecourt/?p=794); [secondary summary of ACMA guidance](https://emaillistvalidation.com/blog/conspicuously-published-address-rule-australian-spam-act/). These are secondary sources, as the ACMA page itself was not retrieved.
- **Airbnb ToS:** It prohibits using members' personal information to send commercial messages. — [Airbnb ToS](https://www.airbnb.com.au/help/article/2908)

### Inferences
- **A compliant outreach stack:**
  - Email or call managers at their published business contacts. The message relates directly to a holiday-letting manager's role, which fits inferred consent.
  - Use letterbox drops or door-knocks for individual owners identified by address. The Spam Act does not cover physical mail. Unaddressed drops avoid using personal names from restricted datasets.
  - Do not use QVAS-derived owner names.
  - Check phone numbers against the Do Not Call Register before calling individuals.

### Gaps
- I did not research CoreLogic/RP Data subscription pricing or sale-listing mining (realestate.com.au / Domain ToS on scraping).
- I did not retrieve ACMA's primary inferred-consent page, or the DNCR rules for B2B numbers.
- Whether Inside Airbnb's "do good with the data" policy tolerates commercial lead generation is unclear. The licence on the download page is CC BY 4.0, but the policies page asks users not to republish the data and states a housing-research mission.
