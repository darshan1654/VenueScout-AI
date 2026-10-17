from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from venuescout.inquiry import build_inquiry_draft
from venuescout.models import Venue


def test_inquiry_draft_contains_event_details():
    draft = build_inquiry_draft(
        Venue(name="Example Venue"),
        {
            "event_type": "Hackathon",
            "city": "Bengaluru",
            "attendees": 150,
            "date": "2026-10-20",
            "duration": "One day",
            "budget": 100000,
        },
    )

    assert "Hello Example Venue Team" in draft
    assert "Preferred date: 2026-10-20" in draft
    assert "Budget: INR 100,000" in draft
