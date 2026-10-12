"""Starter templates. Edit them in the dashboard (Templates); seeding never overwrites edits.

Merge fields available in every template (see templating.context_for):
  greeting_name, account.trading_name, account.registered_name, account.display_name,
  contact.first_name, contact.name, contact.role,
  portfolio.listings, portfolio.houses, portfolio.units, portfolio.first_suburb, portfolio.suburbs,
  hook (AI/hand-written one-liner), property.address, property.suburb,
  sender.*, offer.price, offer.trial
The compliance footer is appended automatically to every email - don't paste it in.
"""
from datetime import datetime, timezone

TEMPLATES = [
    {
        "name": "A1 - Guest bins nobody owns",
        "audience": "business", "angle": "A", "channel": "email",
        "subject": "Bins at your {{ portfolio.first_suburb or 'holiday' }} homes",
        "body": """Hi {{ greeting_name }},

{% if hook %}{{ hook }}

{% endif %}Quick one: who puts the wheelie bins out and brings them back in at your holiday homes{% if portfolio.suburbs %} around {{ portfolio.suburbs }}{% endif %}?

For most managers it's a cleaner squeezing it in, a guest who forgets, or a neighbour who complains. {{ sender.business_short }} is a local family business that specialises in this: bins out before council collection and back in after, twice a week, with a time- and location-stamped photo every visit.

It's {{ offer.price }}, up to 4 bins, no lock-in. Could we prove it with {{ offer.trial }}? You pick the homes that give you the most bin trouble.

Worth 10 minutes this week?

{{ sender.name }}""",
    },
    {
        "name": "B1 - Noosa contact person",
        "audience": "business", "angle": "B", "channel": "email",
        "subject": "One less complaint for your Noosa contact line",
        "body": """Hi {{ greeting_name }},

{% if hook %}{{ hook }}

{% endif %}As a Noosa short-stay manager you're the contact on the property sign and have to respond to complaints within 30 minutes. Bins left on the kerb, or sitting full after a big changeover, are among the easiest complaints to prevent.

{{ sender.business_short }} puts bins out before collection and back in after, twice a week{% if portfolio.suburbs %} across {{ portfolio.suburbs }}{% endif %}, with a time-stamped photo every visit, so if a neighbour does complain you have proof straight away.

{{ offer.price }}, no lock-in. Could we start with {{ offer.trial }}?

{{ sender.name }}""",
    },
    {
        "name": "C1 - Owner-services add-on and bin rooms",
        "audience": "business", "angle": "C", "channel": "email",
        "subject": "Bin rooms and bin runs across your {{ portfolio.first_suburb or '' }} properties",
        "body": """Hi {{ greeting_name }},

{% if hook %}{{ hook }}

{% endif %}Two things we take off managers' plates on the coast:

1. Holiday homes: bins out before council collection and back in after, twice a week, with photo proof for your owner statements.
2. Complexes and bin rooms: scheduled bin presentation plus wheelie-bin cleaning, which cuts the smell and maggot complaints in summer.

Houses are {{ offer.price }}, no lock-in, and we price portfolios as a whole. Would a one-page breakdown for your properties be useful? I can walk you through it in 10 minutes.

{{ sender.name }}""",
    },
    {
        "name": "F1 - Follow-up (day 4)",
        "audience": "business", "angle": "", "channel": "email",
        "subject": "Re: bins at your homes",
        "body": """Hi {{ greeting_name }},

Following up in case this got buried. Happy to send a sample of the photo report owners would see, so you can judge it before any trial. Would that help?

{{ sender.name }}""",
    },
    {
        "name": "F2 - Last follow-up (day 10)",
        "audience": "business", "angle": "", "channel": "email",
        "subject": "Re: bins at your homes",
        "body": """Hi {{ greeting_name }},

I won't keep chasing. If bins ever become a headache (a complaint, a missed collection, an overflowing bin at changeover) we're on {{ sender.phone }} and can usually start within a week.

All the best for the season,
{{ sender.name }}""",
    },
    {
        "name": "O1 - Owner enquiry reply",
        "audience": "owner", "angle": "", "channel": "email",
        "subject": "Your bin service for {{ property.address or 'your property' }}",
        "body": """Hi {{ greeting_name }},

Thanks for getting in touch about {{ property.address or 'your property' }}.

Here's how it works: we put your bins out before council collection{% if property.collection_day %} ({{ property.collection_day }}){% endif %} and bring them back in afterwards, twice a week, with a time-stamped photo after every visit so you can see it's done from anywhere.

It's {{ offer.price }} for up to 4 bins, no lock-in contract{% if offer.trial %}, and holiday rentals on a long-term plan get a 2-week free trial{% endif %}.

Reply to this email or call {{ sender.phone }} and we can start as soon as next collection day.

{{ sender.name }}""",
    },
    {
        "name": "L1 - To the Owner letter",
        "audience": "property_letter", "angle": "", "channel": "letter",
        "subject": "Running your property as short-term accommodation? We'll look after the bins.",
        "body": """The Owner
{{ property.address }}

Dear Owner,

{{ sender.business }} is a local, family-run business on the Sunshine Coast. We help holiday-home owners and managers with one job that's easy to forget: getting the wheelie bins out before council collection and back in afterwards.

Guests often don't know the bin day. Bins left out too long annoy neighbours, and full bins left in are a poor welcome for the next guest. We visit twice a week, handle up to four bins, and send a time- and location-stamped photo of every visit.

- {{ offer.price }}, no lock-in contract
- 2-week free trial for holiday rentals on a long-term plan
- Bin cleaning and rubbish removal for guest changeovers also available

If someone else manages the property for you, feel free to pass this on.
Call {{ sender.phone }} or email {{ sender.email }} and quote {{ letter_code }} for a quote.

Kind regards,
{{ sender.name }}
{{ sender.business }} · {{ sender.website }} · ABN {{ sender.abn }}

We sent this letter because the property is publicly recorded as approved for short-term accommodation. We have not recorded any personal details. If you'd rather not hear from us again, call or email and we'll remove the address.""",
    },
]


def seed(conn) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for t in TEMPLATES:
        conn.execute(
            "INSERT OR IGNORE INTO templates(name, audience, angle, channel, subject, body, updated_at) "
            "VALUES (:name, :audience, :angle, :channel, :subject, :body, :ts)",
            {**t, "ts": ts},
        )
