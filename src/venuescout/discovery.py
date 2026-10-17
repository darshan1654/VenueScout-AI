"""Location-first venue discovery with optional booking-provider links."""

from urllib.parse import urlparse

from .google_places_client import GooglePlacesError, search_physical_venues
from .tinyfish_client import search_web

BLOCKED_DOMAINS = {
    "facebook.com", "instagram.com", "linkedin.com", "youtube.com",
    "youtu.be", "x.com", "twitter.com", "luma.com", "eventbrite.com",
    "townscript.com",
}


def _collect_urls(data: object, discovery_source: str) -> list[dict]:
    """Extract valid URLs from TinyFish Search's nested response format."""
    found = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            url = (
                value.get("url")
                or value.get("link")
                or value.get("website")
                or value.get("website_url")
            )
            if isinstance(url, str):
                parsed = urlparse(url)
                host = (parsed.hostname or "").lower()
                domain = host.removeprefix("www.")
                blocked = any(
                    domain == item or domain.endswith("." + item)
                    for item in BLOCKED_DOMAINS
                )
                if parsed.scheme in {"http", "https"} and host and not blocked:
                    found.append({
                        "name": value.get("title") or value.get("name") or domain,
                        "website_url": url,
                        "discovery_source": discovery_source,
                    })

            for child in value.values():
                if isinstance(child, (dict, list)):
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    return _deduplicate_urls(found)


def _deduplicate_urls(items: list[dict]) -> list[dict]:
    unique = []
    seen = set()
    for item in items:
        parsed = urlparse(item["website_url"])
        key = (parsed.netloc.lower(), parsed.path.rstrip("/"))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def discover_booking_providers(city: str, limit: int = 5) -> list[dict]:
    """Return optional intermediary links, never venue candidates."""
    query = f"venue booking agencies and event venue platforms in {city}"
    try:
        return _collect_urls(search_web(query), "booking_provider_search")[:limit]
    except Exception as exc:
        print(f"Booking-provider search failed: {exc}")
        return []


def _fallback_candidates(fallback_urls: list[str] | None, limit: int) -> list[dict]:
    candidates = []
    for url in fallback_urls or []:
        parsed = urlparse(url.strip())
        if parsed.scheme in {"https", "http"} and parsed.netloc:
            candidates.append({
                "name": parsed.netloc,
                "website_url": url.strip(),
                "discovery_source": "user_provided_fallback",
            })
    return _deduplicate_urls(candidates)[:limit]


def discover_venues(
    city: str,
    event_type: str,
    attendees: int = 150,
    preferred_area: str | None = None,
    limit: int = 5,
    fallback_urls: list[str] | None = None,
    include_booking_providers: bool = False,
) -> tuple[list[dict], list[dict], str]:
    """Discover physical venues first and agencies only as a separate result."""
    providers = (
        discover_booking_providers(city, limit)
        if include_booking_providers
        else []
    )

    try:
        venues = search_physical_venues(
            city=city,
            event_type=event_type,
            attendees=attendees,
            preferred_area=preferred_area,
            limit=limit,
        )
        if venues:
            return venues, providers, "google_places_location_first"
    except GooglePlacesError as exc:
        print(f"Google Places discovery failed: {exc}")

    fallback = _fallback_candidates(fallback_urls, limit)
    method = "user_provided_fallback" if fallback else "no_physical_venues_found"
    return fallback, providers, method
