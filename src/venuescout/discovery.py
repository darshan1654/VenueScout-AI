from urllib.parse import urlparse
from .tinyfish_client import search_web

BLOCKED_DOMAINS = {
    "facebook.com", "instagram.com", "linkedin.com",
    "youtube.com", "youtu.be", "x.com", "twitter.com",
    "luma.com", "eventbrite.com", "townscript.com",
}

VENUE_TERMS = (
    "venue", "conference", "auditorium", "coworking",
    "event space", "convention", "training centre",
    "training center", "banquet", "meeting room",
)

def _collect_urls(data):
    found = []

    def walk(value):
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
                    domain == d or domain.endswith("." + d)
                    for d in BLOCKED_DOMAINS
                )

                if (
                    parsed.scheme in {"http", "https"}
                    and host
                    and not blocked
                ):
                    title = (
                        value.get("title")
                        or value.get("name")
                        or domain
                    )
                    found.append({
                        "name": title,
                        "website_url": url,
                        "discovery_source": "web_search",
                    })

            for child in value.values():
                if isinstance(child, (dict, list)):
                    walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)

    unique = []
    seen = set()

    for item in found:
        parsed = urlparse(item["website_url"])
        key = (parsed.netloc.lower(), parsed.path.rstrip("/"))

        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def discover_venues(
    city,
    event_type,
    attendees=150,
    limit=5,
    fallback_urls=None,
):

    queries = [
        f"official {event_type.lower()} venues conference halls coworking "
        f"spaces in {city} for {attendees} people"
    ]

    candidates = []

    for query in queries:
        try:
            results = search_web(query)
            candidates.extend(_collect_urls(results))
        except Exception as exc:
            print(f"Search failed for '{query}': {exc}")

    # Remove duplicate website paths across all queries.
    unique = []
    seen = set()

    for item in candidates:
        parsed = urlparse(item["website_url"])
        key = (parsed.netloc.lower(), parsed.path.rstrip("/"))

        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Prioritize titles that look like venue businesses.
    def relevance(item):
        text = item["name"].lower() + " " + item["website_url"].lower()
        return sum(term in text for term in VENUE_TERMS)

    unique.sort(key=relevance, reverse=True)

    if unique:
        return unique[:limit], "targeted_web_search"

    # Keep manual URLs as a fallback.
    fallback = []

    for url in fallback_urls or []:
        url = url.strip()
        parsed = urlparse(url)

        if parsed.scheme in {"https", "http"} and parsed.netloc:
            fallback.append({
                "name": parsed.netloc,
                "website_url": url,
                "discovery_source": "user_provided",
            })

    return fallback[:limit], "user_provided_fallback"
