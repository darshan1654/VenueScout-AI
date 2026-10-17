from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from venuescout.models import Venue
from venuescout.scoring import score_venue


def test_score_venue_awards_confirmed_requirements():
    venue = Venue(
        name="Verified Venue",
        capacity_max=200,
        published_price=90000,
        wifi=True,
        power_outlets=True,
        projector_or_display=True,
        catering=True,
        parking=True,
    )

    score, reasons = score_venue(
        venue,
        {
            "attendees": 150,
            "budget": 100000,
            "facilities": [
                "wifi", "power_outlets", "projector_or_display",
                "catering", "parking",
            ],
        },
    )

    assert score == 95.0
    assert "Published capacity meets attendee requirement" in reasons
    assert "Published price is within budget" in reasons


def test_score_venue_does_not_award_unknown_fields():
    venue = Venue(name="Unverified Venue")

    score, reasons = score_venue(
        venue,
        {"attendees": 150, "budget": 100000, "facilities": ["wifi"]},
    )

    assert score == 0.0
    assert "Capacity needs confirmation" in reasons
    assert "Wi-Fi is not verified" in reasons
