import os
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from venuescout.google_places_client import search_physical_venues


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "places": [
                {
                    "id": "place-venue-1",
                    "displayName": {"text": "Example Convention Centre"},
                    "formattedAddress": "1 Main Road, Bengaluru, Karnataka",
                    "location": {"latitude": 12.9716, "longitude": 77.5946},
                    "googleMapsUri": "https://maps.google.com/?cid=1",
                    "websiteUri": "https://example-venue.com",
                    "nationalPhoneNumber": "080 1234 5678",
                    "rating": 4.5,
                    "userRatingCount": 120,
                    "types": ["event_venue", "point_of_interest"],
                },
                {
                    "id": "place-agency-1",
                    "displayName": {"text": "Example Event Management"},
                    "formattedAddress": "2 Main Road, Bengaluru, Karnataka",
                    "googleMapsUri": "https://maps.google.com/?cid=2",
                },
            ]
        }


def test_google_places_returns_physical_venues_not_agencies():
    with patch.dict(os.environ, {"GOOGLE_MAPS_API_KEY": "test-key"}):
        with patch(
            "venuescout.google_places_client.requests.post",
            return_value=FakeResponse(),
        ):
            venues = search_physical_venues(
                city="Bengaluru",
                event_type="Hackathon",
                attendees=150,
            )

    assert len(venues) == 1
    venue = venues[0]
    assert venue["google_place_id"] == "place-venue-1"
    assert venue["address"] == "1 Main Road, Bengaluru, Karnataka"
    assert venue["google_maps_url"] == "https://maps.google.com/?cid=1"
    assert venue["website_url"] == "https://example-venue.com"
    assert venue["discovery_source"] == "google_places"
