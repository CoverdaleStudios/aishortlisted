# Australian / Queensland Legal & Platform Compliance Map for an AI Lead-Generation System (Bin Caddie, Sunshine Coast)

Research date: 10 October 2026. General legal information only, not legal advice. Items marked "VERIFY" were not confirmed against a primary source in this session, and a lawyer (or the regulator's current page) should confirm them before anything is built on them. Two primary pages (acma.gov.au/investigations-spam-and-telemarketing and acma.gov.au/avoid-sending-spam) returned HTTP 503 during research, so some Spam Act detail rests on secondary sources that quote ACMA.

---

## 1. Spam Act 2003 (Cth): commercial email and SMS

### Takeaway
Every commercial email or SMS needs consent (express, or inferred), must identify the sender and must include a working unsubscribe. A cold B2B email to a property manager's *published business address* can rely on "conspicuous publication" inferred consent, but only if the offer is directly relevant to that person's work role, the address carries no "no marketing" statement, and the email meets identify and unsubscribe rules. Cold SMS to a mobile scraped from a listing is high-risk, because a host's mobile is rarely published *in a business-role context* relevant to bin services. ACMA penalties in 2024–2026 have run into the millions.

### Cited Findings
- **Conspicuous-publication inferred consent has three conditions.** (1) The address is conspicuously published. (2) There is no accompanying statement that commercial messages are unwanted. (3) The message is *directly related to the principal role or function* of the recipient. ACMA's wording: "consent may not be inferred from the mere fact that a relevant electronic address has been published." — [ADMA Spam Act overview (quotes ACMA)](https://www.adma.com.au/sites/default/files/Comply%20QA%203%20Spam%20Act%20Overview.pdf); [Itomic summary](https://www.itomic.com.au/?p=3056)
- **ACMA's "washers" example on relevance.** A tap-washer seller "cannot send commercial emails to all businesses with conspicuously published email addresses on the assumption that they all need washers... However, you could send your promotional emails to plumbing supplies stores." A role can be inferred from the address itself (e.g. accounts@business.com) or from where it is published. — [ADMA (quoting ACMA)](https://www.adma.com.au/sites/default/files/Comply%20QA%203%20Spam%20Act%20Overview.pdf); [emaillistvalidation summary](https://emaillistvalidation.com/blog/conspicuously-published-address-rule-australian-spam-act/)
- **Clarity1 case law.** The court required that "it must be reasonable to assume that publication occurred with the agreement of the organization or person involved, and there must be some relevance between the message and the work-related business of the individual or office involved." — [Osgoode "The Court" on ACMA v Clarity1](https://yorku.ca/osgoode/thecourt/?p=794)
- **Identify and unsubscribe still apply.** All messages sent on inferred consent must also meet the Act's identify and unsubscribe conditions. — [ADMA](https://www.adma.com.au/sites/default/files/Comply%20QA%203%20Spam%20Act%20Overview.pdf)
- **The "service message" carve-out is narrow.** "Purely 'service' messages" that are not commercial can be sent without consent or an unsubscribe. ACMA found CBA messages were commercial because they promoted products "or promoted CBA itself". — [ACMA, Commonwealth Bank pays $7.5m (Oct 2024)](https://www.acma.gov.au/articles/2024-10/commonwealth-bank-pays-75m-more-spam-breaches)
- **Enforcement examples (2023–2026):**
  - **Commonwealth Bank: $7.5m (Oct 2024).** More than 170 million emails sent Nov 2022–Apr 2024 with no unsubscribe option; 34.8 million went to people who had not consented or had withdrawn consent. ACMA also accepted an expanded 3-year court-enforceable undertaking. — [ACMA](https://www.acma.gov.au/articles/2024-10/commonwealth-bank-pays-75m-more-spam-breaches)
  - **Commonwealth Bank: $3.55m (May 2023).** About 65 million emails without working unsubscribe (one outlet says 61 million). — [ACMA article above](https://www.acma.gov.au/articles/2024-10/commonwealth-bank-pays-75m-more-spam-breaches); [AdNews](https://adnews.com.au/news/commonwealth-bank-fined-for-sending-170-million-marketing-spam-emails)
  - **Telstra: $626,000 (Mar 2025).** About 10.5 million texts with non-compliant unsubscribe arrangements. ACMA said this was the maximum infringement notice available given the age of the matters. — [ACMA, Telstra penalised for spam breaches](https://www.acma.gov.au/articles/2025-03/telstra-penalised-spam-breaches); [Mi-3](https://www.mi-3.com.au/06-03-2025/acma-whacks-telstra-626000-fine-breaching-australian-spam-laws)
  - **Tabcorp: $4,003,270** infringement notice plus enforceable undertaking (2025; sources disagree on April vs June 2025). — [Privacy108 summary](https://privacy108.com.au/insights/top-acma-penalties-2024-2025/); [EmailExpert](https://emailexpert.com/australia-email-and-sms-compliance-2025-2026-key-acma-penalties-and-lessons-for-marketers/)
  - **Betfair: $871,660** plus EU (July 2025), for emails/SMS sent without consent or a functional unsubscribe. **PointsBet: $500,800** (May 2025). — [Privacy108](https://privacy108.com.au/insights/top-acma-penalties-2024-2025/); [Hall & Wilcox](https://hallandwilcox.com.au/news/regulator-cracks-down-heavy-fines-for-spam-act-violations/)
  - **Lululemon: $702,900** infringement notice (8 Dec 2025) for emails lacking a functional unsubscribe, followed by an enforceable undertaking (Feb 2026). — [EmailExpert](https://emailexpert.com/australia-email-and-sms-compliance-2025-2026-key-acma-penalties-and-lessons-for-marketers/) (secondary; VERIFY on ACMA)
  - Pinsent Masons notes ACMA data shows continuing enforcement focus. — [Pinsent Masons](https://www.pinsentmasons.com/out-law/analysis/acma-australian-scams-report)

### Inferences
- **Cold B2B email to a property manager's published business address** (e.g. rentals@agency.com.au on the agency website) is *likely* compliant on inferred consent. Bin put-out and cleaning for managed rentals relates directly to a property manager's role, so the email must be about that and must identify Bin Caddie (ABN, contact details) and carry a one-click unsubscribe. Check the site for "no unsolicited marketing" wording first. A body-corporate manager's published email is similar. A generic "info@" address at an unrelated business is not.
- **Cold SMS to a host mobile number scraped from Airbnb/Stayz/Google** is high-risk. Conspicuous-publication consent attaches to the "electronic address" in its published context. A personal mobile shown on a listing for *guest* contact is arguably published for guest enquiries, not for receiving supplier marketing. ACMA could find the relevance test unmet. **Recommendation: no cold commercial SMS.** Send SMS only after express opt-in (web form tick-box, or a reply to an inbound enquiry).
- **AI-written emails at scale.** Each message is assessed individually. A system that sends thousands of "relevant-looking" emails to loosely classified addresses risks failing the relevance test across the board. The builder should log the source URL, page context and role for each address as consent evidence.
- **Spam Act ss 20–22 (from background knowledge; VERIFY):** these prohibit supplying, acquiring or using address-harvesting software and harvested-address lists for sending unsolicited commercial messages. A scraper that harvests emails *for* sending unsolicited spam is squarely in this zone. Inferred-consent sends to role-relevant addresses are defensible; untargeted harvested lists are not.

### Gaps
- Primary text of Spam Act s 16 (consent), s 17 (identify), s 18 (unsubscribe), Sch 2 cl 4 (conspicuous publication) and ss 20–22 (harvesting) was not fetched (ACMA site 503). The **5-business-day unsubscribe actioning rule** and the "unsubscribe must work for at least 30 days" rule are from background knowledge (VERIFY: [Spam Act 2003 on legislation.gov.au](https://www.legislation.gov.au/C2004A01214/latest/text)).
- Current maximum civil penalty amounts (penalty units per day, tiered by prior contraventions) were not confirmed. VERIFY on the legislation site.
- No ACMA enforcement example was found involving a *small business* using conspicuous-publication consent for B2B emails.

---

## 2. Do Not Call Register Act 2006 and the Telemarketing Industry Standard 2017: cold calling

### Takeaway
Business numbers cannot be put on the DNCR, but many Airbnb hosts list personal mobiles that may be registered, so any number called must be washed against the DNCR first. All telemarketing calls, including to businesses and by exempt callers, must follow the Telemarketing Standard: calling hours, identification at the start of the call, and calling line identification.

### Cited Findings
- "Business telephone numbers are not eligible for registration." Business fax numbers used primarily for faxing may be registered. Unsolicited telemarketing calls "must not be made or sent" to a registered number. — [donotcall.gov.au consumer overview](https://www.donotcall.gov.au/consumers/consumer-overview/)
- **Telecommunications (Telemarketing and Research Calls) Industry Standard 2017 calling hours.** No telemarketing calls on weekdays before 9am or after 8pm, on Saturdays before 9am or after 5pm, or at any time on Sunday. Times are measured at the called party's location. Calls outside these hours need the account-holder's prior express consent. — [Standard text F2017L00323](https://legislation.gov.au/F2017L00323/asmade/2017-03-28/text/original/pdf); [Herbert Smith Freehills](https://www.herbertsmithfreehills.com/latest-thinking/new-standard-for-telemarketing-and-research-calls)
- **The Standard applies to all telemarketing calls**, including by businesses exempt from the DNCR. Its 2017 changes focused on information given at the start of the call and on calling line identification (CLI). ACMA can impose penalties up to $250,000 for breaches of the standard. — [donotcall.gov.au Industry Standards](https://www.donotcall.gov.au/industry/industry-overview/industry-standards); [ACMA "Remade telemarketing standard"](https://www.donotcall.gov.au/Media-Releases/Remade-telemarketing-standard-what-you-need-to-know)
- **Enforcement:** Lead My Way paid a $285,600 infringement notice for not checking all numbers it called against the DNCR. — [donotcall.gov.au media release](https://donotcall.gov.au/media-releases/do-not-call-crackdown-lead-my-way-pays-285-600). Instyle Solar was also penalised for calling registered numbers. — [donotcall.gov.au](https://www.donotcall.gov.au/Media-Releases/Instyle-Solar-penalised-for-calling-numbers-on-the-Do-Not-Call-Register)

### Inferences
- **Calling an agency's office landline** (a business number) is allowed without DNCR washing, but the Standard still applies: hours, giving the caller's identity and purpose at the start of the call, and showing a CLI number.
- **Calling mobiles scraped from listings or Google profiles:** treat these as potentially private numbers. Wash every number against the DNCR. VERIFY the wash-validity period; one vendor claims 30 days. Keep wash records, and don't call registered numbers without consent. Lead My Way shows failing to wash is itself the breach.
- **Public holidays:** the Standard is generally understood to bar calls on national public holidays as well (VERIFY in the Standard's text).

### Gaps
- Exact DNCR Act s 11 penalty amounts and whether a "business mobile" of a sole-trader host counts as a business number were not confirmed. The register's eligibility test turns on how the number is used, so a lawyer should confirm.
- The DNCR wash-validity period (commonly cited as 30 days) was not confirmed from a primary source.

---

## 3. Privacy Act 1988 (Cth) and APPs: coverage, the small business exemption, the 2024 amendments and tranche 2

### Takeaway
Bin Caddie (turnover under $3m) is generally exempt from the APPs. **The exemption is lost if it trades in personal information**: buying a lead list, selling or sharing leads, or collecting personal information for a benefit. Selling a lead database or tool to others almost certainly brings the vendor under the Act. The statutory privacy tort (from 10 June 2025) applies to *everyone*, including small businesses. The OAIC has had infringement-notice powers since 10 Dec 2024. Automated-decision transparency in privacy policies applies from 10 Dec 2026. The small business exemption had **not** been removed as of October 2026.

### Cited Findings
- **Small business exemption.** Section 6D of the Privacy Act defines a small business as one with annual turnover of $3 million or less in the previous financial year. It falls back under the Act if it discloses personal information for a "benefit, service or advantage", or provides one to collect it. OAIC example: a small business that "sells their customer list to a marketing company or gives their own list in return for another list." — [OAIC Privacy business resource 10](https://www.oaic.gov.au/agencies-and-organisations/business-resources/privacy-business-resource-10); [OAIC small business (archived)](https://www.oaic.gov.au/_old/privacy/privacy-for-organisations/small-business); [PM Lawyers](https://www.pmlawyers.com.au/blog/2016/12/employment-law-and-workplace-relations-blog/privacy-laws-and-the-sale-of-personal-information-by-businesses/)
- **Opting in.** Small businesses can choose to be treated as an APP entity under s 6EA. — [OAIC opting in](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/opting-in-to-the-privacy-act)
- **Statutory tort commenced 10 June 2025.** It is a standalone cause of action for serious invasions of privacy by intrusion on seclusion or misuse of private information. The plaintiff must show a reasonable expectation of privacy, intent or recklessness, and seriousness, and the court weighs the public interest. — [LexisNexis](https://www.lexisnexis.com/blogs/en-au/insights/australias-bold-leap-into-a-new-era-of-privacy-law); [MinterEllison](https://www.minterellison.com/articles/privacy-and-other-legislation-amendment-act-2024-now-in-effect)
- **OAIC infringement and compliance notice powers** from 10 Dec 2024. — [FTI Consulting](https://www.fticonsulting.com/es-es/spain/insights/articles/australian-privacy-law-reforms-take-effect); [Norton Rose Fulbright](https://www.nortonrosefulbright.com/de-de/wissen/publications/be98b0ff/australian-privacy-alert-parliament-passes-major-and-meaningful-privacy-law-reform)
- **Automated decision-making transparency.** APP entities must disclose in privacy policies the use of automated decisions that significantly affect individuals. Two-year grace period ending 10 December 2026 (one source says 11 Dec 2026). — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/de-de/wissen/publications/be98b0ff/australian-privacy-alert-parliament-passes-major-and-meaningful-privacy-law-reform); [Mondaq](https://www.mondaq.com/australia/privacy-protection/1640630/australias-ongoing-privacy-reforms-bolstering-australias-privacy-regulatory-framework)
- **Tranche 2 status (Oct 2026).** The small business exemption is still law. The government agreed "in principle" to remove it (Sept 2023 response) but has set no timetable. One source reports an exposure draft "Privacy Amendment (Personal Data Protection) Bill 2026" released 31 Aug 2026 that keeps the exemption; **unverified**, and other Sept/Oct 2026 sources describe no bill. — [CoterieLabs](https://coterielabs.com.au/field-notes/privacy-act-small-business-exemption-not-removed-2026); [Ashurst Perkins Coie](https://www.ashurstperkinscoie.com/en/insights/australias-2026-privacy-reforms-a-first-look-at-pivotal-new-changes/); [Aitken](https://www.aitken.com.au/news/privacy-act-reforms-tranche2); [IDCARE](https://www.idcare.org/learning-centre/fact-sheets/what-to-do-if-your-business-has-been-breached)
- **Related change.** From 1 July 2026, AML/CTF tranche 2 brings real estate agents and others under AML/CTF reporting. The OAIC estimates more than 100,000 small businesses become Privacy Act-covered as a result. This matters because many Bin Caddie *prospects* (real estate/property managers) are now APP entities. — [search summary of OAIC estimate via biztechlawyers/rulesmate](https://rulesmate.com.au/insights/privacy-act-second-tranche-reforms-2026-outlook) (VERIFY with OAIC)

### Inferences
- **Bin Caddie operating alone** (turnover under $3m, collecting leads for its own use, not buying or selling lists) is likely exempt from the APPs. Even so, following the APPs (privacy policy, APP 7-style direct-marketing opt-outs, data security) is low-cost and future-proofs against tranche 2.
- **Buying a scraped lead list from a vendor**, or swapping lists with a partner (e.g. a cleaner), is "collecting for a benefit" and risks losing the exemption.
- **A software vendor selling a lead database or tool** is almost certainly "trading in personal information", or is over $3m, so the APPs apply. In particular: APP 3 (collection only by lawful and fair means; scraping in breach of site terms may be "unfair"), APP 5 (notice), APP 7 (direct marketing: individuals must be able to opt out, and the source of the information must be disclosed on request) and APP 8 (offshore disclosure, e.g. to US AI APIs). VERIFY APP 3/7 detail against the [OAIC APP Guidelines](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines).
- **The tort risk to Bin Caddie is low** for ordinary marketing. It rises with intrusive tactics, e.g. linking a camera image of a person's home to their name and phone for unsolicited contact.

### Gaps
- Did not verify the exact text of the reported 31 Aug 2026 exposure draft. Treat tranche 2 timing as unknown.
- No OAIC infringement notice issued against a small marketing or lead-gen business was found.

---

## 4. Web scraping and platform terms (Airbnb, Stayz/Expedia, Booking.com, Google, LinkedIn)

### Takeaway
Airbnb's Terms (updated 5 Feb 2026) expressly ban bots and scrapers. They also ban using its messaging tools or members' personal information to send commercial messages without express consent. **Do not scrape Airbnb or solicit hosts through Airbnb messaging.** Google Maps Platform terms allow only temporary caching (e.g. Places lat/lng up to 30 days). Australian law has no specific anti-scraping statute; risk comes from contract (browsewrap vs clickwrap), copyright, the Privacy Act (APP 3 for covered entities) and the Spam Act's harvesting rules.

### Cited Findings
- **Airbnb Terms of Service (Last Updated 5 Feb 2026), s 11.1:**
  - "Do not use bots, crawlers, scrapers, or other automated means to access or collect data or other content from or otherwise interact with the Airbnb Platform."
  - "You may only use another Member's personal information as necessary to facilitate a transaction."
  - "Do not use the Airbnb Platform, our messaging tools, or Members' personal information to send commercial messages without [the recipient's] express consent."
  - s 21: Irish governing law, but mandatory local consumer protections may apply.
  - — [Airbnb Terms of Service (airbnb.com.au help 2908)](https://www.airbnb.com.au/help/article/2908); [ConductAtlas record of bot clause, verified May 2026](https://conductatlas.com/platform/airbnb/airbnb-terms-of-service/provision/CA-P-021897/prohibition-on-bots-and-automated-platform-access/)
- **Airbnb off-platform policy** prohibits moving bookings off Airbnb and links that lead off-platform in messages. Repeated or severe breaches can lead to suspension or deactivation. — [Airbnb help article 2799](https://www.airbnb.ca/help/article/2799)
- **Airbnb API access** is limited to partner "API Programs". Its API terms reportedly bar using API content to scrape, keep static copies or build databases unless authorised. — [Octoparse summary](https://www.octoparse.com/blog/airbnb-api-data-access-options) (secondary)
- **Enforceability in Australia** depends on how the terms are presented. Account-based clickwrap acceptance is generally stronger than browsewrap. — [Sprintlaw web scraping guide](https://sprintlaw.com.au/articles/web-scraping-essential-australian-legal-guidelines/)
- **Google Maps Platform Service Specific Terms:** customers may temporarily cache Places API latitude/longitude "for up to 30 consecutive calendar days". Place IDs may be stored per the Places API Policies. Similar 30-day limits apply to Geocoding, Directions and Roads. — [Maps Service Terms archive 2025-05-01](https://cloud.google.com/archive/maps-platform/terms/maps-service-terms-20250501); [archive 2025-03-31](https://cloud.google.com/archive/maps-platform/terms/maps-service-terms-20250331)

### Inferences
- **Airbnb:** creating an account to message hosts with a bin-service pitch breaches s 11.1. Expect account removal; it may also be an unsolicited commercial electronic message under the Spam Act. Collecting host names and numbers by scraper breaches the bot clause. Off-limits.
- **Allowed alternatives:** manually viewing public listings to understand *where* holiday rentals cluster (aggregate geography, no personal data harvested); advertising in host communities that permit it; partnering with Airbnb co-hosts or property managers; paid ads targeting "Airbnb host Sunshine Coast".
- **Google Places API:** fine for finding *businesses* (property-management agencies, body-corporate managers) and their published business phone and website. Don't build a permanent shadow database of Places content beyond the caching limits. Re-query or store only place_id. Contacting those businesses is governed by Spam Act/DNCR rules above, not Google terms.
- **Stayz/Expedia, Booking.com, LinkedIn:** these terms were not fetched in this session. Background knowledge: all three prohibit automated scraping in their user terms. LinkedIn's User Agreement bans scraping and automated messaging, and LinkedIn actively bans accounts. US hiQ v LinkedIn litigation is not Australian law. Treat all three as **off-limits for scraping** (VERIFY current terms).

### Gaps
- Could not retrieve the current Google Maps Platform Service Specific Terms page (fetch truncated). Street View-specific restrictions (bulk download, image analysis or derived datasets) are **unverified**. Background understanding: the Google Maps Platform Terms prohibit scraping, bulk download and creating content derived from Google Maps Content, which would cover running CV over Street View imagery to build a lead list (VERIFY at [cloud.google.com/maps-platform/terms](https://cloud.google.com/maps-platform/terms)).
- No Australian court decision squarely on commercial web scraping enforceability was located.
- Stayz/Expedia Group, Booking.com and LinkedIn terms were not fetched.

---

## 5. Vehicle or dashcam computer vision to detect bins left out, and Street View imagery

### Takeaway
Queensland's Invasion of Privacy Act 1971 regulates *listening* devices only. Filming from a public street with a video-only camera is not prohibited by Queensland surveillance law. Images tied to street addresses may still be "personal information" (for APP-covered entities) and could feed tort risk if used intrusively. Recording **audio** of private conversations is the real legal tripwire. Google Street View imagery should not be scraped or machine-analysed (VERIFY terms).

### Cited Findings
- The Invasion of Privacy Act 1971 (Qld) regulates listening devices that overhear, record or monitor private conversations. It "does not regulate the use of any optical, tracking or data surveillance device." Aggrieved people rely on the Criminal Code (Qld) or common-law trespass/nuisance. The QLRC recommended replacing it with a Surveillance Devices Bill. The consolidated Act was current as at 1 July 2024, so reform is apparently not enacted (VERIFY). — [Invasion of Privacy Act 1971 (Qld) current](https://www.legislation.qld.gov.au/view/whole/html/current/act-1971-050); [Mallesons/KWM "The future of surveillance law in Queensland"](https://www.mallesons.com/au/en/insights/latest-thinking/the-future-of-surveillance-law-in-queensland)
- The statutory tort (from 10 June 2025) covers "intrusion on seclusion" and "misuse of private information" where there is a reasonable expectation of privacy and the invasion is serious. — [LexisNexis](https://www.lexisnexis.com/blogs/en-au/insights/australias-bold-leap-into-a-new-era-of-privacy-law)

### Inferences
- **Video-only dashcam CV that detects wheelie bins on the kerb** and records only the street address (no faces, no plates, no audio) is likely lawful in Queensland. Reasonable expectation of privacy for a bin on a public kerb is low. Design choices that reduce risk: disable audio, blur faces and plates at the edge, discard raw frames after detection, store only "address + date + bins-out flag".
- **Is "street address + bin photo" personal information?** Under the Privacy Act an address can be personal information where an individual is reasonably identifiable, e.g. once linked to an owner name from a title search. Bin Caddie is likely exempt (section 3). A vendor selling this as a dataset would be covered and would need APP 3/5/7 compliance.
- **Use for letterbox drops only** (no addressed contact) is the lowest-risk application. Avoid stating "we saw your bins out on 3 Oct" in marketing. It reads as surveillance, invites complaints and edges toward tort "intrusion" framing.
- **Local road rules and driver distraction:** camera rigs must not obstruct driver view (VERIFY Queensland Transport Operations (Road Use Management) rules). This is an operational, not marketing, issue.
- **Google Street View as the data source:** treat as off-limits for automated analysis unless Google terms are confirmed to permit it (see Gaps in section 4).

### Gaps
- OAIC guidance on whether images of residential frontages or house numbers are personal information was not fetched.
- Queensland Criminal Code provisions (e.g. s 227A observations/recordings in breach of privacy, which focuses on private acts/states) were not verified.

---

## 6. Letterbox drops, "No Junk Mail" signs and addressed mail

### Takeaway
Unaddressed letterbox drops are legal but should respect "No Junk Mail" / "No Advertising Material" signs, per the industry Distribution Standards Board (DSB) code and Australia Post practice. Addressed mail to "The Owner/Occupier" is ordinary postal mail and isn't covered by the Spam Act or DNCR.

### Cited Findings
- The DSB, set up by the catalogue/distribution industry, publishes a Code of Practice under which advertising material should not go into letterboxes displaying a refusal sign. The DSB takes complaints. — [City of Ryde "No Advertising Mail stickers"](https://www.ryde.nsw.gov.au/Environment-and-Waste/Waste-and-Recycling/Other-Services/Litter-and-Illegal-Dumping/No-Advertising-Mail-Stickers); [ACT Hansard 2002](https://hansard.act.gov.au/hansard/5th-assembly/2002/HTML/week13/3783.htm)
- Australia Post delivery staff are instructed not to deliver unaddressed mail to letterboxes marked "No Junk Mail" or "Addressed Mail Only". — [Australia Post junk mail](https://auspost.com.au/personal/receiving/mail-redirection-and-mail-hold/junk-mail)
- The Queensland Government has a page on unsolicited advertising material (junk mail) under litter laws. It lists the DSB contact as 1300 083 241; Ryde Council lists 1800 676 136 (conflict). — [qld.gov.au junk mail](https://www.qld.gov.au/environment/circular-economy-waste-reduction/litter-illegal-dumping/junk-mail)

### Inferences
- **Do:** honour No Junk Mail signs; include identity and contact details on flyers; don't leave material where it will blow away. Queensland litter law (Waste Reduction and Recycling Act 2011) treats loose unsolicited advertising as potential littering (VERIFY via the qld.gov.au page).
- **Addressed mail to the owner name from a title search:** not regulated by the Spam Act. Privacy Act issues arise only if Bin Caddie is an APP entity. Check title-search conditions (section 8).

### Gaps
- DSB Code text and whether the DSB is still active (or is now a different body) as of 2026 were not verified.

---

## 7. AI voice agents and AI SMS

### Takeaway
Australian law has no AI-specific telemarketing rule. An outbound AI voice call is treated like any telemarketing call: DNCR washing for private numbers, the Telemarketing Standard (hours, identification, CLI), and the ACL against misleading conduct. AI SMS is a commercial electronic message under the Spam Act. **Inbound** AI receptionists that answer customer-initiated calls are low-risk.

### Cited Findings
- The rules (DNCR Act, Spam Act, Telemarketing Standard 2017) were written for human callers and recorded messages but are broad enough to catch AI voice without naming it. Inbound AI answering is not telemarketing. — [Trillet (vendor blog)](https://trillet.ai/blogs/australia-do-not-call-register-and-ai-voice-calls) (secondary; not an ACMA source)
- The Telemarketing Standard requires specified information at the start of each call and calling line identification. — [ACMA "Remade telemarketing standard"](https://www.donotcall.gov.au/Media-Releases/Remade-telemarketing-standard-what-you-need-to-know)

### Inferences
- **Disclose that the caller is an AI** at the start of the call. This isn't confirmed as an express statutory requirement, but leaving a person believing they are talking to a human could be misleading conduct under ACL s 18. It is also a likely future ACMA/ACCC focus.
- **Recording calls:** in Queensland, a party to a conversation may record it under the Invasion of Privacy Act. Other states differ (e.g. a NSW-based landlord requires consent of all parties under the Surveillance Devices Act 2007 (NSW)). For interstate owners, announce recording (VERIFY).
- **AI SMS** must have consent, sender identification and an unsubscribe (reply STOP), the same as any SMS.

### Gaps
- No ACMA primary guidance specific to AI-generated voice was found as of Oct 2026.

---

## 8. Council registers and Titles Queensland searches

### Takeaway
No public Noosa short-stay register of owner contact details was found. Approved properties must display an approval notice with a contact number, but that contact exists for *complaints*. Title searches reveal owner names. The Land Title Act restricts commercial use of fee-free government searches, but no general statutory ban on marketing use by private searchers was found.

### Cited Findings
- **Noosa short-stay local law:** each approved premises must nominate a contact person (which can be a letting agent or property manager) who is based within 20km, reachable 24/7 and responds to complaints within 30 minutes. An approval notice with the approval number and dedicated phone number must be displayed at the front of the property. — [Noosa conditions of approval](https://noosa.qld.gov.au/downloads/file/4312/conditions-of-approval-short-stay-letting); [Noosa Short Stay Letting](https://www.noosa.qld.gov.au/short-stay-letting)
- **Land Title Act 1994 (Qld) s 284(7):** the registrar may agree to fee-free searches for departments only if satisfied the information won't be used commercially, expressly including "marketing or sale", or added to another database without approval. — [AustLII s 284](https://classic.austlii.edu.au/au/legis/qld/consol_act/la199448/s284.html)

### Inferences
- **Calling or texting the complaints contact number on a Noosa approval sign to pitch bin services** is contrary to the purpose of the publication. It probably fails Spam Act relevance for SMS, and since many contact persons are property managers, cold calls are better made to agency landlines. However, the Noosa scheme does signal that **local property managers are the gatekeepers** for short-stay properties. Target them via their business channels.
- **Title searches:** using purchased title data to address mail to owners is not expressly prohibited by statute on the evidence found. However, Titles Queensland and resellers (InfoTrack etc.) have terms of use that may restrict marketing use, and bulk title-data reselling for marketing may fall within APP "trading" (VERIFY the Titles Queensland conditions of use).

### Gaps
- Did not confirm whether Sunshine Coast Council (as distinct from Noosa) runs a public short-term accommodation register.
- Titles Queensland's search terms and conditions were not fetched.

---

## 9. Australian Consumer Law: AI-generated marketing claims and reviews

### Takeaway
ACL s 18 (misleading or deceptive conduct) and s 29 (false representations, including fake testimonials) apply to AI-written copy exactly as to human copy. Fake or business-written reviews have attracted Federal Court penalties. Every AI-generated claim must be substantiated, and testimonials must be real.

### Cited Findings
- **Service Seeking** was ordered to pay $600,000. It admitted to falsely representing that about 17,000 reviews were by customers when businesses created them via a template feature. — [ACCC media release](https://www.accc.gov.au/media-release/service-seeking-to-pay-penalty-for-misleading-online-customer-reviews)
- **Euro Solar and Australian Solar Panel:** combined $125,000 in penalties for fake testimonials. **Live Life Alarms:** a $25,200 infringement notice for a fake testimonial. The ACCC says it is illegal to create fake reviews or arrange for others to. — [HWL Ebsworth](https://hwlebsworth.com.au/penalties-for-fake-testimonials-and-false-refund-promises/); [ACCC online reviews guidance](https://www.accc.gov.au/business/advertising-and-promotions/online-product-and-service-reviews)
- **US analogue:** the FTC final order against Rytr over an AI "Testimonial & Review" generator. — [FTC](https://www.ftc.gov/node/86996)

### Inferences
- **Don't:** let the AI invent testimonials, star ratings, "trusted by 200 hosts" counts, council-endorsement claims, or "eco"/"hospital-grade" cleaning claims without evidence. Don't gate or incentivise only positive reviews.
- **Do:** keep a substantiation file for each claim (price, response times, sanitising chemicals); human-review AI copy before sending; and disclose AI voice and chat agents.
- **Current ACL maximum penalty for companies** (from background knowledge, VERIFY): the greater of $50m, 3x the benefit, or 30% of adjusted turnover. Infringement notices for small businesses are much smaller.

### Gaps
- No 2025–2026 ACCC case specifically about AI-generated reviews in Australia was found.

---

## Summary compliance map (tactic, status, conditions)

| Tactic | Status | Key conditions / source |
|---|---|---|
| Cold email to a property manager / body-corporate manager at their published business address | ALLOWED (inferred consent) | Must be directly relevant to their role; no "no spam" notice; identify + unsubscribe — ACMA via ADMA, Clarity1 |
| Cold email to generic/unrelated published addresses, or bulk harvested lists | OFF-LIMITS | Fails relevance; Spam Act harvesting rules (VERIFY ss 20–22) |
| Cold SMS to host mobiles scraped from listings | OFF-LIMITS in practice | Relevance/consent risk; DNCR; Airbnb terms |
| SMS/email after web-form opt-in | ALLOWED | Record express consent; identify + unsubscribe |
| Cold calling agency office landlines | ALLOWED | Telemarketing Standard hours (wkdays 9–8, Sat 9–5, no Sun), ID, CLI |
| Cold calling mobiles | CONSENT or DNCR WASH | Wash against DNCR; Standard applies |
| Outbound AI voice calls | Same as human telemarketing, plus disclose AI | DNCR + Standard + ACL |
| Scraping Airbnb / messaging hosts via Airbnb | OFF-LIMITS | Airbnb ToS s 11.1 (5 Feb 2026) |
| Scraping Stayz/Booking/LinkedIn | OFF-LIMITS (VERIFY terms) | Platform ToS |
| Google Places API to find agencies | ALLOWED within terms | Caching ≤30 days lat/lng; place_id storable |
| CV on Street View imagery | OFF-LIMITS pending terms check | Google Maps Platform Terms (VERIFY) |
| Own video-only dashcam CV for bins-out to target letterbox drops | LIKELY ALLOWED | No audio (Qld IPA 1971); minimise data; avoid intrusive messaging |
| Unaddressed letterbox drops | ALLOWED | Respect No Junk Mail (DSB code, AusPost) |
| Addressed "Owner/Occupier" mail | ALLOWED | Not Spam Act; check title-data terms |
| Buying/selling/swapping lead lists | Triggers Privacy Act | Small business exemption lost (s 6D trading) |
| AI-written ads and reviews | ALLOWED if true | ACL ss 18, 29; no fake reviews |
