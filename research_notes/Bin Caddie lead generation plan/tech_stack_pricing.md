# Tech Stack, Comparable Products & Commercial Pricing for an AI Lead-Gen System for Local Home/Property Service Businesses (AU) — first customer Bin Caddie (Sunshine Coast, QLD)

Research date: 10 October 2026. Unless marked AUD, prices are **USD** list prices from US-based vendors. Australia Post prices are AUD (the page does not say whether GST is included). No USD→AUD rate was sourced; convert at the live rate when budgeting (roughly 1.5 AUD/USD is a working assumption only — verify). Many figures come from third-party aggregators, and this is flagged throughout.

## Q1. Data, enrichment and scraping tools (2026)

### Takeaway
For one region like the Sunshine Coast, lead data is cheap. Apify actors (about $0.50–$4 USD per 1k results) and the Google Places API (New) free monthly caps cover Airbnb listings and Google Maps business lists for a few dollars a month. Clay ($185+/mo) is only worth paying for once the system serves several clients. Australian property data (CoreLogic/Cotality, Domain, Pricefinder) has no public self-serve pricing and needs sales contact or enterprise contracts.

### Cited Findings
**Apify — Google Maps**
- Apify's official Google Maps Scraper (compass/crawler-google-places) is pay-per-event, "from $1.50 / 1,000 scraped places". Store discounts apply, and higher subscription plans get lower prices. — [Apify actor page](https://apify.com/compass/crawler-google-places)
- Derived per-unit add-on prices on that page (FREE plan / SILVER plan): additional place details $0.002 / $0.0015; company contacts enrichment (emails, phones and socials scraped from the business website) $0.002 / $0.0015; reviews $0.0005 / $0.00037; social profile enrichment $0.10 / $0.007. A "business leads enrichment" add-on returns full name, work email, mobile, job title and LinkedIn. An email-verification add-on is charged only for ok/invalid/disposable results. — [Apify actor page](https://apify.com/compass/crawler-google-places)
- An older Apify help article quoted $0.004 per place (about $4/1k), plus $0.001 per filter per place and a run-start fee. This conflicts with the current "from $1.50/1k" headline, which suggests the price has dropped or now depends on plan. — [Apify Help](https://help.apify.com/en/articles/10774732-google-maps-scraper-is-going-to-pay-per-event-pricing); [Apify blog 2026](https://blog.apify.com/best-google-maps-scrapers/)
- The Apify free plan includes $5 of usage credit a month. — [Apify Airbnb actors via search summary](https://apify.com/tri_angle/new-fast-airbnb-scraper)

**Apify — Airbnb (community actors)**
- Prices vary by actor: Tri⟁angle "Fast Airbnb Scraper" about $0.50/1k results; Cirkit "Airbnb Search Scraper" from $0.50/1k; Crawlio "Airbnb Listings Scraper" from $0.75/1k; s-r "Airbnb Scraper" about $2.50/1k; ayeeyee "Airbnb Scraper" $3.00–$3.50/1k; full-year price tracker $7/1k. — [tri_angle](https://apify.com/tri_angle/new-fast-airbnb-scraper); [cirkit](https://apify.com/cirkit/airbnb-search-scraper); [crawlio](https://apify.com/crawlio/airbnb-listings-scraper); [s-r](https://apify.com/s-r/airbnb-scraper); [ayeeyee](https://apify.com/ayeeyee/airbnb-scraper)

**Outscraper**
- Third-party sources: about $3/1k Google Maps records after a monthly free allowance of 500 records, and $1/1k above 100k. Enriched leads (Maps + emails + verification) are about $7–$15/1k. Sources conflict on the free contacts allowance (500 vs 25 emails). — [SyncGTM review 2026](https://syncgtm.com/blog/outscraper-review-2026); [FitGap](https://us.fitgap.com/products/outscraper)

**Google Places API (New) — official pricing page**
- Text Search Pro: 5,000 free/month, then $32.00 per 1k. Text Search Enterprise: 1,000 free, then $35/1k. Nearby Search Pro: 5,000 free, then $32/1k. Nearby Search Enterprise: 1,000 free, then $35/1k. Place Details Essentials: 10,000 free, then $5/1k. Place Details Pro: 5,000 free, then $17/1k. Place Details Enterprise: 1,000 free, then $20/1k. ID-only SKUs are unlimited/free. — [Google Maps Platform pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- Free caps are per SKU and reset monthly; they are not pooled. Requests bill at the highest SKU triggered by the field mask, so asking for name, address and location already lands in the Pro tier. — [OpenPlacesAPI explainer](https://openplacesapi.com/blog/google-places-api-pricing)
- The pricing page says nothing about caching or storage terms. (Google Maps Platform terms generally restrict long-term storage of Places content; not verified in this research, see Gaps.) — [Google pricing page](https://developers.google.com/maps/billing-and-pricing/pricing)

**Clay**
- Free: 100 Data Credits and 500 Actions a month, tables capped at 200 rows, no phone enrichment. Launch: $185/mo monthly or $167/mo annual, with 2,500 Data Credits and 15,000 Actions. Growth: $495/mo monthly or $446/mo annual; most sources say 6,000 credits and 40,000 Actions, one says unlimited, so this conflicts. Growth adds CRM sync. Enterprise median is about $30.4k/yr (Vendr data). A March 2026 overhaul split usage into "Data Credits" and "Actions". Top-up credits reportedly cost 50% more than plan rate. — [Valley 2026](https://www.joinvalley.co/blog/clay-pricing-and-credits-explained-2026); [Zeliq (competitor)](https://www.zeliq.com/blog/clay-pricing); [Landbase](https://www.landbase.com/blog/clay-pricing)
- Waterfall enrichment means querying 150+ providers in sequence until one returns data. — [Valley](https://www.joinvalley.co/blog/clay-pricing-and-credits-explained-2026)

**Email finders**
- Hunter.io (as of Aug 2026): Free (50 credits/mo); Starter $34/mo annual or $49 monthly; Growth $104/$149; Scale $209/$299; Enterprise custom. Accuracy is strongest at large companies with structured email formats and weaker for SMBs and non-English markets. — [MarketBetter](https://marketbetter.ai/blog/hunter-io-pricing-breakdown-2026/); [BounceZero review](https://bouncezero.io/hunter-io-review-2026)
- Apollo paid plans are about $49–$149/user/mo (third-party), with a 200M+ contact database. The official pricing page was not retrieved. — [Cleanlist comparison](https://www.cleanlist.ai/blog/2026-03-07-hunter-vs-apollo); [Apollo vs Hunter (vendor)](https://www.apollo.io/insights/apollo-vs-hunterio)

**Australian property data**
- Domain runs a self-serve developer portal (developer.domain.com.au). The "Agents & Listings" and "Properties & Locations" packages are included on sign-up. Listings Management and Price Estimation are added per project and negotiated with an account manager. Agency enquiry and performance data needs the agency to authorise the app. No prices are published. — [Domain Developer FAQ](https://developer.domain.com.au/docs/v1/support/faq/)
- CoreLogic, rebranded Cotality, publishes no self-service pricing. The developer portal is documentation only; live data needs an enterprise contract. RP Data packages are listed on corelogic.com.au without public API pricing. — [apis.io CoreLogic](https://apis.io/plans/corelogic/corelogic-plans-pricing/); [CoreLogic AU packages](https://www.corelogic.com.au/legals/rp-data-packages)
- No public API pricing was found for Pricefinder (owned by Domain). — [Domain AGM 2019](https://shareholders.domain.com.au/FormBuilder/_Resource/_module/T9NtqvJX0UGSmtpsWXgLcA/file/presentations/AGM-Presentation-2019.pdf)

**STR market data APIs**
- AirROI quotes pricing for data and API services per partner; there is no public rate card. — [Software Advice AU – AirROI](https://www.softwareadvice.com.au/software/527983/AirROI)
- BNBCalc REST API: $0/mo, $0.20 per successful report. — [BNBCalc API pricing](https://www.bnbcalc.com/rest-api/pricing)
- AirDNA MarketMinder was $99/mo Basic and $199/mo Pro in 2023, and Airbtics $49–$399/mo in 2023. These figures are stale. Airbtics now sells pay-as-you-go endpoints. — [Datarade 2023](https://datarade.ai/top-lists/best-airbnb-apis); [IPS/BNBCalc comparison](https://ipsnews.net/business/?p=248120)

### Inferences
- A full Sunshine Coast pull of all STR listings plus all property managers, real estate agencies and body corporate managers on Google Maps is likely 5k–15k records. On Apify that costs under about $50 USD per full refresh. The Places API free caps (5,000 Text Search Pro + 10,000 Place Details Essentials a month) alone may cover monthly refreshes of the B2B list at $0.
- Airbnb listings show only approximate pin locations and host first names, so scraped STR data identifies *who manages* (the host or co-host company) better than *which street address*. The B2B route (property managers and co-hosts managing many listings) is the efficient play: one manager equals many bins. Address-level targeting needs other signals, such as drive-by surveys, letterbox drops or council STR registers.
- Clay is overkill for one local client. Apify/Outscraper contacts enrichment plus Hunter's free or Starter tier (about $34–$49 USD/mo) is enough. Add Clay Launch only when the system serves several clients.
- Hunter's and Apollo's weak SMB/AU coverage means website scraping (Apify contacts enrichment) will likely beat database lookups for small Sunshine Coast property managers.

### Gaps
- Apify's exact base "place scraped" price per plan was not shown explicitly on the actor page.
- No primary source checked on Apollo, Snov or Lusha 2026 pricing or Australian coverage. No source quantified AU small-business email coverage for any of them.
- Google Places terms on caching and storing data for lead lists were not verified.
- No pricing was found for Pricefinder, realestate.com.au (REA has no public API for third parties to my knowledge, unverified), CoreLogic, Domain paid packages, AirDNA or Airbtics 2026.
- SerpAPI pricing was not researched.

## Q2. Outreach and CRM (email, CRM, SMS, direct mail)

### Takeaway
GoHighLevel is the default agency stack in AU: $97–$497 USD/mo, with SaaS mode at $497 to resell under your own brand and an AI Employee add-on at about $97/sub-account/mo. Cold email tools run $39–$97/mo. Australia Post Unaddressed Mail is AUD 40.5c per small letterbox item (same-state standard), targetable by postcode or suburb. AU cold email has to comply with the Spam Act's inferred-consent rules.

### Cited Findings
**GoHighLevel**
- Agency Starter $97/mo (3 sub-accounts), Agency Unlimited $297/mo, Agency Pro/SaaS Pro $497/mo (SaaS configurator: rebrand, set your own client pricing tiers, rebill usage). — [GHL Experts](https://ghlexperts.com/gohighlevel-plans-pricing); [RSLA](https://rsla.io/blog/go-high-level-pricing)
- The AI Employee bundle (Voice AI, Conversation AI, Reviews AI, Content AI, Funnel AI, Workflow AI) is about $97/mo per sub-account, "unlimited" AI usage. SMS, email, phone and voice are billed from usage wallets (e.g. phone credits about $0.015/segment cited). Typical all-in: solo on Starter $115–$140/mo; Unlimited plus AI Employee and real volume $440–$600/mo. — [RSLA](https://rsla.io/blog/go-high-level-pricing); [App Pricing Lab](https://saas.apppricinglab.com/product/gohighlevel/); [Ecosire](https://ecosire.com/blog/gohighlevel-pricing-worth-it-2026)

**Cold email**
- Instantly: entry about $47/mo, with 2026 bundles Starter $94 / Scale $194 / Agency $555 per one source, or Starter $47 / Scale $97 per another, so the sources conflict. Unlimited mailboxes and warmup. Smartlead: Base $39/mo; Pro $94/mo with API and webhooks; white-label client workspaces $29/mo each. Lemlist: about $55–$109/user/mo, the only one of the three with native LinkedIn and calling. — [Valley comparison](https://www.joinvalley.co/blog/instantly-vs-smartlead-vs-lemlist); [Instantly (vendor)](https://instantly.ai/blog/instantly-vs-smartlead-lemlist-2026/); [SmartReach](https://smartreach.io/blog/instantly-vs-smartlead-vs-lemlist/)

**Spam Act 2003 (AU) compliance**
- Inferred consent from a conspicuously published address applies only if the address has no "no commercial messages" statement and the message relates directly to the recipient's role or line of business. Publication alone is not enough. Every message needs accurate sender ID and a working unsubscribe. Breaches carry civil penalties. — [Spam Act 2003 (legislation.gov.au)](https://www.legislation.gov.au/C2004A01214/2016-03-10/2016-03-10/text/original/epub/OEBPS/document_1/document_1.html); [Lawpath](https://lawpath.com.au/blog/common-email-marketing-tactics-that-are-actually-illegal/2); [EmailListValidation](https://emaillistvalidation.com/blog/conspicuously-published-address-rule-australian-spam-act/)

**SMS (AU)**
- Twilio AU: outbound SMS $0.0515/segment, inbound $0.0075, MMS $0.35. AU mobile number $8.25/mo. Alphanumeric sender ID is free (outbound only). Plus a $0.001 failed-message fee and carrier fees. Currency is not stated on the page; Twilio usually lists USD. — [Twilio AU SMS pricing](https://www.twilio.com/en-us/sms/pricing/au)
- ClickSend AU: pay-as-you-go top-up tiers (Boost from $20; Growth $500 saves 7%; Scale $3,000 saves 14%; Enterprise $10,000 saves 21%). Inbound replies are free and carrier fees are extra. The live page did not render per-SMS rates. ClickSend's Post (letters) product is "no longer available to new customers". — [ClickSend AU pricing](https://www.clicksend.com/au/pricing/au/)
- A third-party table lists ClickSend AU at $0.0092/SMS (2025 data, currency unclear). This looks low next to typical AU rates and should be treated as unreliable. — [Sent.dm](https://www.sent.dm/en/resources/sms-pricing/australia-sms-pricing)

**Direct mail / Unaddressed Mail (AUD, Australia Post)**
- Standard service (delivery within 15 business days), per item. Small ≤50g: same state $0.405, other state $0.470. Small 50–100g: $0.685 / $0.835. Large ≤50g: $0.635 / $0.718. Large 50–100g: $0.945 / $1.100. — [Australia Post Unaddressed Mail](https://auspost.com.au/business/shipping/letters/domestic-sending/large-volume-letters/bulk-mail-options/unaddressed-mail)
- Premium (same state, delivery within 7 business days): Small ≤50g $0.516; Large ≤50g $0.809. Short-week premium applies in public-holiday weeks. Contract rates are available for large volumes. No-show fee is $140 for bookings up to 5,000 articles. — [Australia Post UMS](https://auspost.com.au/business/shipping/letters/domestic-sending/large-volume-letters/bulk-mail-options/unaddressed-mail)
- Targeting is by postcode or suburb. "Regular" covers street and roadside points at minimum. "Select" lets you exclude those or customise beyond postcode/suburb. The free Campaign Targeter tool maps campaigns. The page does not say round- or walk-level targeting is available. Reach is 9.3M letterboxes for advertising out of 12.7M total delivery points; the rest display "No Advertising Material". Small item size is 88×138mm to 130×240mm (DL/C6). Standard same-state lodgement is due by 12 noon, 5 business days before the delivery week. — [Australia Post UMS](https://auspost.com.au/business/shipping/letters/domestic-sending/large-volume-letters/bulk-mail-options/unaddressed-mail)
- UMS prices rose 31 Oct 2025 and again 1 July 2026 (per the Post Charges Guide). Peak-period delivery changes apply 2 Nov 2026 – 1 Jan 2027. — [AusPost pricing update May 2026](https://auspost.com.au/disruptions-and-updates/pricing-updates/apr-pricing-update-2026)

### Inferences
- For Bin Caddie, a GHL sub-account (CRM, pipelines, SMS, two-way inbox, booking, review requests) is the natural "system" to deploy and resell. In SaaS mode you can rebill wallet usage at a markup.
- A 10,000-letterbox DL flyer drop in Sunshine Coast holiday postcodes (e.g. beachside suburbs) costs about AUD $4,050 in postage (small ≤50g, same state, standard), plus print. It suits body-corporate and holiday-let dense streets, but it can't separate STR from owner-occupied homes.
- Cold email to property managers and body corporate managers is defensible under the Spam Act if it is sent to their published business addresses and is about property services, which relates to their role. Cold email to individual Airbnb hosts' personal addresses is riskier.

### Gaps
- HubSpot, Pipedrive, MessageMedia (Sinch) and Postgrid AU pricing were not researched. No Lob-equivalent addressed-mail API for AU with confirmed pricing was found (ClickSend Post is closed to new customers).
- AusPost doesn't say whether UMS prices include GST, and doesn't confirm delivery-round-level targeting.
- No confirmed per-SMS AUD ClickSend rate.

## Q3. AI layer (LLMs, voice agents, computer vision)

### Takeaway
LLM cost per lead is negligible (fractions of a cent with Haiku/Sonnet-class models). Voice agents cost about $0.07–$0.31 USD/min all-in, and AU telephony and numbers add cost. Computer vision for wheelie-bin detection is feasible, but public datasets are small, so expect to collect and label local images.

### Cited Findings
- Anthropic list prices (per 1M tokens, input/output, USD; model table cached 6 Oct 2026): Claude Haiku 5.5 $0.10/$0.50 (≤100K-token prompts); Claude Sonnet 5.5 $2/$10; Claude Opus 5.5 $4/$20. The Batch API runs asynchronously at 50% cost. — [Anthropic pricing](https://docs.claude.com/en/docs/about-claude/pricing) (figures from the Claude API skill reference dated 2026-10-06)
- Vapi: $0.05/min orchestration only, with LLM, STT, TTS and carrier billed separately. Estimated all-in $0.13–$0.31/min. Retell: $0.07–$0.31/min advertised (voice engine $0.07–$0.08/min), Twilio telephony $0.015/min, numbers $2/mo (verified number $10/mo). International destination calling is $0.03–$0.80/min. Concurrency is $8 per concurrent call/mo beyond 20 on pay-as-you-go. Bland: $0.11–$0.14/min including STT, LLM and TTS (another source says $0.09). Synthflow: from $0.09/min, with enterprise about $0.08/min. — [MorphLLM matrix](https://www.morphllm.com/comparisons/vapi-vs-retell-vs-bland-vs-synthflow); [eesel Retell pricing](https://eesel.ai/blog/retell-ai-pricing); [Retell pricing](https://www.retellai.com/es/pricing); [Techsy](https://techsy.io/sv/blogg/ai-voice-agent-priser-2026)
- GHL's AI Employee includes Voice AI and Conversation AI (website chat, SMS and social DM bots) at about $97/sub-account/mo, so a separate chat widget is not needed if GHL is used. — [RSLA](https://rsla.io/blog/go-high-level-pricing)
- Roboflow Universe has small, CC BY 4.0 bin datasets, e.g. a "wheelie bin + white garbage truck" detector (no description), "yolo-p2" (road/garbage/bin/pavement), "PFE-Bin-Detection" (151 images), and "bin-prototype-3" (YOLOv11, 82 images). None is clearly a large kerbside wheelie-bin dataset. — [Roboflow LuhTask](https://universe.roboflow.com/luh-gh57q/poc...); [yolo-p2](https://universe.roboflow.com/project-blmh9/yolo-p2); [PFE-Bin-Detection](https://universe.roboflow.com/pfe-ejqeu/pfe-bin-detection); [bin-prototype-3](https://universe.roboflow.com/adams-workspace-0l4qa/bin-prototype-3)

### Inferences
- Personalising 5,000 outreach emails (about 2k input + 300 output tokens each) costs well under USD $5 on Haiku 5.5 and about $35 on Sonnet 5.5, less with Batch.
- AI voice is best used *inbound* (answering after-hours quote calls, qualifying, booking) rather than for cold outbound calling to AU consumers, which brings Do Not Call Register and telemarketing standard obligations (not researched here).
- A drive-by survey that detects bins left on the kerb after collection day (a signal of absentee or holiday owners) is a novel lead signal. It needs a custom-labelled YOLO model fine-tuned from a few hundred local dashcam frames. Public datasets are too small or generic. Privacy (number plates, faces) and Sunshine Coast-specific data would need care.

### Gaps
- No AU-specific pricing for Vapi/Retell/Bland/Synthflow phone numbers or AU per-minute rates.
- Dashcam hardware costs and the legality of drive-by surveys (Privacy Act, Surveillance Devices Act QLD) were not researched.
- No research on agent frameworks (n8n, LangGraph, etc.) or OpenAI/Gemini pricing.

## Q4. Local SEO and inbound (GBP, LSA, landing pages, Meta ads)

### Takeaway
I found no evidence that Google Local Services Ads are available in Australia, so inbound should rely on Google Business Profile, programmatic suburb pages and Meta lead ads. Meta CPLs in AU consumer categories are typically about AUD $20–$35 (directional data).

### Cited Findings
- Third-party LSA guides list available countries as the US, UK, Canada and several EU markets. Australia is not listed, and no source confirms AU availability. — [Enrich Labs LSA guide 2026](https://www.enrichlabs.ai/blog/local-services-ads-complete-guide-2026); [Search Engine Land](https://searchengineland.com/google-expands-local-services-ads-categories-ahead-of-migration-485695)
- Meta CPL in Australia (Oct 2024 – Oct 2025, superads.ai vendor data): Real Estate about 23.28 (vs global 36.04); Marketing about 18.42; Wellness about 31.81; Retail about 57.78. General guidance: B2C CPL usually $10–$50. — [Superads Real Estate AU](https://www.superads.ai/facebook-ads-costs/cost-per-lead/real-estate/australia); [Superads Wellness AU](https://www.superads.ai/facebook-ads-costs/cost-per-lead/wellness-holistic-health/australia)
- AU agency SEO retainers are about $1,200–$2,500/mo; results take 3–6 months. — [Prospeo AU lead gen](https://prospeo.io/s/lead-generation-australia); [BFJ Digital](https://bfj.digital/insights/how-much-does-a-digital-marketing-agency-cost-in-australia/)

### Inferences
- For bin valet, the inbound wins are: a GBP with "Bin cleaning service" or similar categories plus service areas covering each Sunshine Coast suburb; programmatic pages ("Bin put-out service Noosa Heads / Mooloolaba / Caloundra…") tied to council collection-day data; and Meta lead ads targeted at property owners and holiday-let hosts in 45xx postcodes. Expected CPL is probably AUD $15–$40 for a low-ticket B2C service (inference from the categories above, not a sourced benchmark).

### Gaps
- No AU home-services or cleaning-specific Meta CPL benchmark was found. Google's LSA help pages were not checked directly for AU. No GBP optimisation benchmarks were researched.

## Q5. Comparable products and benchmarks (agency pricing, pay-per-lead, STR software integrations)

### Takeaway
AU agencies typically charge $1,500–$4,000 AUD/mo per channel plus $2.5k–$15k for CRM setup. hipages-style marketplaces charge tradies about $21 per lead on average plus a membership. In the US, PropStream/BatchLeads-style list SaaS runs $99–$749 USD/mo. Hostaway and Guesty both run partner marketplaces with API keys (Breezeway, Turno and TIDY are listed for cleaning), so a bin-service integration is technically plausible via partner API.

### Cited Findings
**Agency and lead pricing (AU)**
- Australian businesses typically pay agencies $2,000–$15,000/mo; startups $1,500–$5,000/mo; a single channel for an SMB $1,000–$4,000/mo. SEO retainers $1,200–$2,500/mo. Google Ads management $1,200–$3,500/mo plus ad spend. CRM setup and integration is a $2,500–$15,000 project plus licences. Outreach-only lead-gen retainers $2.5k–$5k/mo; strategy plus execution $6k–$10k/mo (B2B-oriented). 78% of agencies publish no prices. — [Prospeo](https://prospeo.io/s/lead-generation-australia); [BFJ Digital](https://bfj.digital/insights/how-much-does-a-digital-marketing-agency-cost-in-australia/)
- Exclusive-territory lead subscriptions are advertised at a flat $500/mo + GST (web-design niche, marketing page). — [Whatsthedamage](https://whatsthedamage.com.au/agencies/wordpress/perth/)
- hipages: average lead about $21, varying with trade, location and job size. 2026 plans range from "Essentials" ($29/mo) to a Pro plan ($2,049/mo) per PricingSaaS. Older sources say members pay $40–$200/mo plus lead credits. In H1 FY26 all tradies moved to new pricing plans with ARPU growth. — [Brainbound](https://www.brainbound.blog/hipages-cost-guide); [PricingSaaS hipages](https://pricingsaas.com/companies/hipagesgroup); [hipages H1 FY26 ASX](https://announcements.asx.com.au/asxpdf/20260224/pdf/06wn9bmw8wbt28.pdf)

**US list/data SaaS benchmarks**
- PropStream (2026): $99 / $199 / $699 per month billed monthly ($81 / $165 / $583 annual). BatchLeads: $119 / $349 / $749 per month (vendor blog). PropStream acquired BatchLeads and BatchDialer in July 2025. BatchDialer is from $95/agent/mo (March 2026). — [PropStream](https://www.propstream.com/news/how-much-does-propstream-cost); [BatchLeads blog](https://batchleads.io/blog/batchleads-vs-propstream-how-to-choose-the-best-leads-software); [RISMedia](https://www.rismedia.com/2026/03/25/propstreams-batchdialer-introduces-reduced-simplified-pricing-plans/)

**STR operations software and marketplaces**
- Turno: free for hosts using marketplace cleaners; about $8–$10/property/mo to manage your own cleaners; takes cleaner-side and platform fees. — [Capterra Turno](https://www.capterra.com/p/166734/Turno/pricing/); [STR Specialist](https://strspecialist.com/reviews/turno-cleaning-marketplace-review)
- Breezeway: Host Essentials $19.99/mo, other plans not disclosed. An aggregator estimates $2–$8/property/mo (unverified). — [PricingSaaS Breezeway](https://pricingsaas.com/companies/breezeway); [LatestCost](https://latestcost.com/breezeway-software-cost-pricing/)
- Hostaway Marketplace has 100+ to 200+ partner integrations (counts differ by page). Partners connect via API keys the PM generates in the dashboard, with two-way API data flow. The Cleaning Management category includes Breezeway, Turno, TIDY (vendor coordination, automated billing for service providers) and Hostvisors (custom API work). — [Hostaway support](https://support.hostaway.com/hc/en-us/articles/4406922627611-Hostaway-Marketplace); [Hostaway TIDY](https://hostaway.com/marketplace/tidy); [Hostaway glossary](https://www.hostaway.com/glossary/hostaway-marketplace/)
- Guesty Marketplace has 200+ vendors. Marketplace partners connect with a Marketplace API key that expires 4 hours after generation, separate from Open API/OAuth keys. Open API is REST (listings, reservations, calendar, messaging, webhooks) using OAuth2 client credentials with 24h tokens, max 5 tokens per key per day. One third-party report claims marketplace partners need commercial approval. — [Guesty Help](https://help.guesty.com/hc/en-gb/articles/9371576143389-Guesty-API-key-for-Marketplace-partners); [Guesty API](https://www.guesty.com/features/api); [Supergood report card](https://supergood.ai/api-report-card/guesty)

### Inferences
- A sellable package for a local service business in AU could be priced at **AUD $1,500–$5,000 setup plus $500–$1,500/mo** for a "done-for-you AI lead system" (GHL CRM + scraped lead lists + automated email/SMS sequences + AI inbound responder + monthly letterbox campaign management). The alternative is **pay-per-qualified-lead at about $25–$60** (above hipages' about $21 average because leads are exclusive and pre-qualified) or **pay-per-signed-customer at about $100–$200** (see LTV, Q6). This range is triangulated from the agency retainer, setup-fee and hipages figures above and is not a sourced benchmark.
- As a productised SaaS (GHL SaaS mode), comparable US list tools at $99–$749 USD/mo suggest a "local lead finder" for service businesses could sell at about AUD $149–$499/mo per client.
- PMS integration: a bin service could connect to Hostaway or Guesty as a marketplace partner, reading reservations or checkouts and calendars to schedule bin put-out and cleaning around guest turnovers. A low-effort path is reading PM calendars via iCal or using the PM's own Open API key. A full marketplace listing needs a partnership application. This positions Bin Caddie the way cleaning vendors on Turno and Breezeway are positioned.

### Gaps
- Hospitable, Lodgify and Avantio API and marketplace details were not researched, and no evidence was found on which PMS Sunshine Coast managers actually use.
- No published AU pay-per-lead prices for agency lead-gen in home services (only hipages). Airtasker fees were not researched.
- No US "STR lead list" vendor pricing (lists of Airbnb hosts sold to service providers) was found.
- No AU bin valet competitor pricing was found (searches returned only bin-storage valet services such as Boxly at $12/mo and MyStorage at $24/mo in Melbourne, which are a different service). — [Inside Self-Storage](https://www.insideselfstorage.com/self-storage-industry-news/valet-self-storage-startup-boxly-launches-in-melbourne-australia)

## Q6. Customer lifetime value economics for an ~$80/mo (ex GST) bin valet subscription

### Takeaway
At AUD $80/mo ($960/yr), revenue lifetime value is about $1,600–$4,000 depending on monthly churn (5% down to 2%). Under the 3:1 LTV:CAC rule and an assumed 50% gross margin, a sustainable CAC is about AUD $270–$670 per residential subscriber, and several times that for a property manager with many properties. No bin-valet-specific churn data was found.

### Cited Findings
- Average customer lifetime in months ≈ 1 / monthly churn. CAC = sales and marketing spend ÷ new customers. A healthy LTV:CAC is ≥3:1; below 1:1 loses money. With a 6-month CAC payback, monthly churn must be below about 16% to recover CAC. — [Vindicia CLV:CAC guide](https://vindicia.com/resources/guides/a-practical-guide-to-a-healthy-clv-cac-ratio-and-subscription-business-growth/); [Stripe churn 101](https://stripe.com/en-be/resources/more/subscription-churn-101)
- Annual billing is cited as the single biggest retention lever (DTC supplements context). — [EightX](https://eightx.co/blog/average-subscription-of-revenue-for-dtc)

### Inferences (worked numbers, AUD ex GST — the assumptions are mine)
| Monthly churn | Avg lifetime | Revenue LTV | Gross-profit LTV @50% GM | Max CAC @3:1 |
|---|---|---|---|---|
| 2% | 50 mo | $4,000 | $2,000 | ~$667 |
| 3% | 33 mo | $2,667 | $1,333 | ~$444 |
| 5% | 20 mo | $1,600 | $800 | ~$267 |
- A property manager or body corporate account covering 10–30 properties or bin banks multiplies LTV 10–30×, so a CAC of AUD $2k–$10k per PM account is justified. B2B outreach (email, LinkedIn, phone, PMS partnership) is the highest-leverage channel.
- Holiday-let churn drivers include properties sold, owners switching managers, and STR regulation changes, so churn may be higher than for owner-occupied subscribers. Annual prepay discounts and contracts with PMs (not individual owners) reduce it.
- A lead system priced at about AUD $1,000/mo needs about 2–4 new residential subscribers a month (at 3% churn, LTV about $2,667) or one PM account per quarter to clear 3:1.

### Gaps
- No industry churn, gross margin or CAC data specific to bin cleaning or bin valet businesses (AU or US) was found. Bin Caddie's actual route cost, margin and churn should replace the assumptions above.
- Sunshine Coast STR listing counts and council STR regulation were not researched here.
