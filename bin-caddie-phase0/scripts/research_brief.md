# Research brief: Sunshine Coast short-stay manager accounts (Bin Caddie Phase 0)

You are building a B2B account sheet for Bin Caddie (bincaddie.com.au), a Sunshine Coast business that puts holiday-rental wheelie bins out before council collection and brings them back in ($80/month ex GST per home, 2 visits/week, time-stamped photo proof, no lock-in, 2-week free trial), plus bin cleaning and bin-room service for complexes.

For EACH host in your batch JSON file, identify the business behind the Airbnb host name and record ONLY published BUSINESS contact details.

## Rules (legal - Spam Act 2003, Airbnb Terms, Privacy Act)
- Do NOT fetch or scrape airbnb.com.au / airbnb.com pages. Use the host_about text provided, plus web search and the business's OWN website, Google Business listing snippets, Tourism Noosa / Visit Sunshine Coast directories, ABN Lookup.
- Record only contact details the business itself publishes (website contact page, footer, Google Business Profile). Record the exact URL where each email/phone was found (this is the Spam Act "conspicuous publication" evidence).
- Note if the page says anything like "no unsolicited marketing / no sales calls" -> set no_marketing_notice = yes.
- Prefer role addresses (info@, reservations@, admin@, owners@). Record a named person (e.g. principal, owner, operations manager) only if their name AND role are published on the business's own site or LinkedIn company page; never personal mobiles unless published as the business's line.
- If a host name is just a first name (e.g. "Michelle") and you cannot confidently link it to a business from host_about + search, mark status = "individual - do not contact by name" and stop. Do not guess identities.

## Fields per account (output one row each)
host_name | business_name | website | business_type (letting agency / real estate agency w holiday rentals / co-host / resort manager / other) | office_suburb | published_email | email_source_url | published_phone | phone_source_url | decision_maker (name - role - source_url, or blank) | no_marketing_notice (yes/no/unknown) | portfolio_notes (listing count on own site, suburbs, houses vs units, owner-services page?) | current_bin_or_cleaning_mentions (any mention of bins/waste/cleaning in their owner services) | pitch_angle (1-2 sentences tailored hook for Bin Caddie) | confidence (high/med/low) | status

## Output
Write a CSV (with header, quote all fields) to the output path given, and also a short markdown summary of notable findings. Be efficient: ~3-6 tool calls per account.
