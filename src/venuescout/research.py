
import json

from .models import Venue
from .tinyfish_client import research_website


def research_venue(candidate: dict, event: dict) -> Venue:
    website = candidate["website_url"]

    validation_goal = f"""
Visit {website} and determine whether this website
represents a physical event venue or a business that
offers event spaces in {event.get("city", "Bengaluru")}.

Return JSON only:
{{
  "is_venue": true,
  "venue_name": null,
  "official_venue_website": null,
  "reason": ""
}}

Set is_venue to true only when the website provides
evidence that this is an actual venue or event-space
provider. A past hackathon page, event registration
page, social media page, or general news article alone
is not sufficient.

Do not guess. If uncertain, set is_venue to false.
"""

    from .tinyfish_client import research_website

    validation = research_website(website, validation_goal)

    if isinstance(validation, str):
        import json
        validation = json.loads(validation)

    if not isinstance(validation, dict) or not validation.get("is_venue"):
        raise ValueError(
            f"Candidate is not verified as a venue: {website}"
        )

    goal = f"""
You are researching an event venue for an organizer.

Visit this website and navigate relevant pages when useful:
{website}

Event requirements:
- Event type: {event.get("event_type", "Hackathon")}
- City: {event.get("city", "Bengaluru")}
- Expected attendees: {event.get("attendees", 150)}
- Event date: {event.get("date", "Not specified")}
- Budget ceiling: INR {event.get("budget", 100000)}

Extract ONLY information explicitly supported by this website.

Return one JSON object with these keys:
{{
  "name": null,
  "website_url": "{website}",
  "source_urls": [],
  "address": null,
  "area": null,
  "capacity_min": null,
  "capacity_max": null,
  "published_price": null,
  "price_currency": "INR",
  "price_notes": null,
  "wifi": null,
  "power_outlets": null,
  "projector_or_display": null,
  "catering": null,
  "parking": null,
  "contact_phone": null,
  "contact_email": null,
  "date_availability": null,
  "evidence_notes": [],
  "unknown_fields": []
}}

Rules:
- Use null for unknown values.
- Boolean facility fields must be true, false, or null.
- Do not guess prices, capacity, amenities, or availability.
- Do not treat a general event page as confirmation of the requested date.
- Include URLs of pages that support the extracted facts in source_urls.
- Add important missing fields to unknown_fields.
- Use published prices only; explain quote-only pricing in price_notes.
- Return JSON only, with no Markdown fences.
"""

    result = research_website(website, goal)

    # The agent may wrap the requested object in a result field.
    if isinstance(result, dict) and "raw_result" in result:
        raise ValueError(
            f"Could not parse structured result for {website}: "
            f"{result['raw_result']}"
        )

    if isinstance(result, dict):
        for key in ("venue", "data", "result"):
            if isinstance(result.get(key), dict):
                result = result[key]
                break

    if isinstance(result, str):
        result = json.loads(result)

    if not isinstance(result, dict):
        raise ValueError(f"Unexpected result for {website}")

    result.setdefault("name", candidate.get("name", "Unknown venue"))
    result.setdefault("website_url", website)
    result.setdefault("source_urls", [website])

    result["research_status"] = "researched"

    # Ensure required lists have safe defaults.
    result.setdefault("evidence_notes", [])
    result.setdefault("unknown_fields", [])

    venue = Venue.model_validate(result)
    return venue
