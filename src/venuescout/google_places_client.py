"""Minimal Google Places API (New) client for physical venue discovery."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = ",".join(
    (
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.location",
        "places.googleMapsUri",
        "places.websiteUri",
        "places.nationalPhoneNumber",
        "places.rating",
        "places.userRatingCount",
        "places.types",
    )
)


class GooglePlacesError(Exception):
    pass


def _headers() -> dict[str, str]:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise GooglePlacesError(
            "GOOGLE_MAPS_API_KEY is missing. Add it to your .env file."
        )

    return {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }


def _is_booking_provider(place: dict) -> bool:
    """Keep agencies out of the physical-venue shortlist."""
    name = place.get("displayName", {}).get("text", "").lower()
    provider_terms = (
        "event planner",
        "event management",
        "booking agency",
        "venue booking",
        "wedding planner",
    )
    return any(term in name for term in provider_terms)


def _to_candidate(place: dict, search_area: str) -> dict:
    location = place.get("location") or {}
    display_name = place.get("displayName") or {}

    return {
        "name": display_name.get("text") or "Unknown venue",
        "website_url": place.get("websiteUri"),
        "google_place_id": place.get("id"),
        "google_maps_url": place.get("googleMapsUri"),
        "address": place.get("formattedAddress"),
        "area": search_area,
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "google_rating": place.get("rating"),
        "google_review_count": place.get("userRatingCount"),
        "place_types": place.get("types") or [],
        "contact_phone": place.get("nationalPhoneNumber"),
        "discovery_source": "google_places",
    }


def search_physical_venues(
    city: str,
    event_type: str,
    attendees: int,
    preferred_area: str | None = None,
    limit: int = 5,
) -> list[dict]:
    """Return Google Places results that represent named physical locations."""
    search_area = preferred_area.strip() if preferred_area else city.strip()
    query = f"{event_type} venue for {attendees} people in {search_area}"

    try:
        response = requests.post(
            TEXT_SEARCH_URL,
            headers=_headers(),
            json={"textQuery": query, "languageCode": "en"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GooglePlacesError(f"Google Places search failed: {exc}") from exc

    candidates = []
    seen_place_ids = set()

    for place in response.json().get("places", []):
        place_id = place.get("id")
        # A complete address and a Google Maps URI identify a real location.
        if (
            not place_id
            or place_id in seen_place_ids
            or not place.get("formattedAddress")
            or not place.get("googleMapsUri")
            or _is_booking_provider(place)
        ):
            continue

        seen_place_ids.add(place_id)
        candidates.append(_to_candidate(place, search_area))

        if len(candidates) >= limit:
            break

    return candidates
