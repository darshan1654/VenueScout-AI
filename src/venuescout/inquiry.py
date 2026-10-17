
def build_inquiry_draft(venue, event: dict) -> str:
    venue_name = venue.name

    return f"""Subject: Venue Inquiry for {event.get("event_type", "Event")}

Hello {venue_name} Team,

I am planning a {event.get("event_type", "event")} in
{event.get("city", "Bengaluru")} and would like to enquire about
hosting it at your venue.

Event details:
- Expected attendees: {event.get("attendees", 150)}
- Preferred date: {event.get("date", "To be confirmed")}
- Duration: {event.get("duration", "One day")}
- Budget: INR {event.get("budget", 100000):,}

Could you please confirm:
1. Availability for the requested date.
2. Total venue rental cost, including taxes and deposits.
3. Maximum capacity and suitable seating arrangements.
4. Wi-Fi and power outlet availability.
5. Projector or display equipment availability.
6. Catering options and parking facilities.
7. Any additional charges, restrictions, or booking conditions.

Please share a quotation and any relevant venue information.

Thank you,
Event Organizer
"""
