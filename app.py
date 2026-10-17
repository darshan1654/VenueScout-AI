
import sys
import json
from pathlib import Path
from datetime import date
from urllib.parse import urlencode

import streamlit as st

# Allow Python to import modules from src/venuescout.
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from venuescout.discovery import discover_venues
from venuescout.research import research_venue
from venuescout.scoring import score_venue
from venuescout.inquiry import build_inquiry_draft

st.set_page_config(
    page_title="VenueScout AI",
    page_icon="📍",
    layout="wide",
)

st.title("📍 VenueScout AI")
st.write(
    "Discover, research, and compare event venues using "
    "TinyFish-powered website research."
)

with st.sidebar:
    st.header("Event requirements")

    event_type = st.selectbox(
        "Event type",
        ["Hackathon", "Seminar / Conference", "Workshop", "Wedding"],
    )

    city = st.text_input("City", "Bengaluru")
    attendees = st.number_input(
        "Expected attendees", min_value=1, value=150
    )
    budget = st.number_input(
        "Maximum venue budget (₹)",
        min_value=0,
        value=100000,
        step=5000,
    )
    event_date = st.date_input("Preferred date", value=date.today())
    duration = st.selectbox(
        "Duration", ["Half day", "One day", "Multiple days"]
    )

    facility_labels = {
        "Wi-Fi": "wifi",
        "Power outlets": "power_outlets",
        "Projector / display": "projector_or_display",
        "Catering": "catering",
        "Parking": "parking",
    }

    selected_facilities = st.multiselect(
        "Required facilities",
        list(facility_labels.keys()),
        default=list(facility_labels.keys()),
    )

    fallback_text = st.text_area(
        "Optional fallback venue URLs",
        placeholder="Paste one official venue website URL per line",
        help="Used if automatic venue discovery fails.",
    )

event = {
    "event_type": event_type,
    "city": city,
    "attendees": int(attendees),
    "budget": float(budget),
    "date": event_date.isoformat(),
    "duration": duration,
    "facilities": [
        facility_labels[label] for label in selected_facilities
    ],
}

fallback_urls = [
    line.strip()
    for line in fallback_text.splitlines()
    if line.strip()
]

if st.button("🔎 Discover and research venues", type="primary"):
    if not city.strip():
        st.error("Please enter a city.")
        st.stop()

    with st.spinner("Discovering candidate venue websites..."):
        candidates, discovery_method = discover_venues(
            city=city.strip(),
            event_type=event_type,
            attendees=int(attendees),
            limit=3,
            fallback_urls=fallback_urls,
        )

    st.write("Discovery method:", discovery_method)

    if not candidates:
        st.warning(
            "No venue websites were discovered. Paste a few official "
            "venue URLs in the sidebar and try again."
        )
        st.stop()

    st.write(f"Found {len(candidates)} candidate website(s).")

    researched_venues = []
    progress = st.progress(0)

    for index, candidate in enumerate(candidates):
        name = candidate.get("name", candidate["website_url"])
        st.write(f"Researching {index + 1}/{len(candidates)}: {name}")

        try:
            venue = research_venue(candidate, event)
            venue.match_score, venue.match_reasons = score_venue(
                venue, event
            )
            researched_venues.append(venue)

        except Exception as exc:
            st.warning(
                f"Could not research {candidate['website_url']}: {exc}"
            )

        progress.progress((index + 1) / len(candidates))

    # Save the successfully researched results locally.
    data_dir = PROJECT_ROOT / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / "venue_results.json"
    output_path.write_text(
        json.dumps(
            [venue.model_dump(mode="json") for venue in researched_venues],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    st.session_state["venues"] = [
        venue.model_dump(mode="json") for venue in researched_venues
    ]
    st.session_state["event"] = event

if "venues" in st.session_state:
    venues = st.session_state["venues"]

    st.divider()
    st.header("Venue comparison")

    if not venues:
        st.info("No venues were successfully researched in this run.")
    else:
        venues.sort(
            key=lambda item: item.get("match_score") or 0,
            reverse=True,
        )

        rows = []

        for venue in venues:
            rows.append({
                "Venue": venue.get("name"),
                "Match score": venue.get("match_score"),
                "Published price (₹)": venue.get("published_price"),
                "Capacity": venue.get("capacity_max") or "Not verified",
                "Wi-Fi": venue.get("wifi"),
                "Power": venue.get("power_outlets"),
                "Projector": venue.get("projector_or_display"),
                "Catering": venue.get("catering"),
                "Parking": venue.get("parking"),
            })

        st.dataframe(rows, use_container_width=True)

        for venue in venues:
            with st.expander(
                f"{venue.get('name', 'Unknown venue')} — "
                f"{venue.get('match_score', 0)}/100"
            ):
                website = venue.get("website_url")

                st.write("Address:", venue.get("address") or "Not verified")
                st.write(
                    "Published price:",
                    venue.get("published_price")
                    if venue.get("published_price") is not None
                    else "Quote required / not published",
                )
                st.write(
                    "Date availability:",
                    venue.get("date_availability") or "Not confirmed",
                )

                st.write("Why this score?")
                for reason in venue.get("match_reasons", []):
                    st.write(f"- {reason}")

                st.write("Evidence notes:")
                for note in venue.get("evidence_notes", []):
                    st.write(f"- {note}")

                st.write(
                    "Unknown fields:",
                    ", ".join(venue.get("unknown_fields", []))
                    or "None reported",
                )

                st.write("Source URLs:")
                for url in venue.get("source_urls", []):
                    st.markdown(f"- [{url}]({url})")

                from venuescout.models import Venue

                venue_model = Venue.model_validate(venue)
                inquiry = build_inquiry_draft(
                    venue_model, st.session_state["event"]
                )

                # These actions deliberately hand control back to the user:
                # no email is sent and no booking is made by VenueScout AI.
                action_columns = st.columns(3)

                if website:
                    action_columns[0].link_button(
                        "Visit venue / booking page",
                        website,
                        use_container_width=True,
                    )

                contact_email = venue.get("contact_email")
                if contact_email:
                    email_link = (
                        f"mailto:{contact_email}?"
                        + urlencode({
                            "subject": (
                                f"Venue Inquiry for "
                                f"{st.session_state['event']['event_type']}"
                            ),
                            "body": inquiry,
                        })
                    )
                    action_columns[1].link_button(
                        "Email enquiry draft",
                        email_link,
                        use_container_width=True,
                    )
                else:
                    action_columns[1].caption(
                        "No published email address"
                    )

                contact_phone = venue.get("contact_phone")
                if contact_phone:
                    action_columns[2].link_button(
                        "Call venue",
                        f"tel:{contact_phone}",
                        use_container_width=True,
                    )

                st.text_area(
                    "Inquiry draft",
                    value=inquiry,
                    height=260,
                    key=f"inquiry_{venue.get('name')}",
                )

        st.caption(
            "Scores are preliminary rule-based matches. Confirm prices, "
            "facilities, and event-date availability directly with each venue."
        )
