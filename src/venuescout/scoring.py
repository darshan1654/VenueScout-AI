
def score_venue(venue, requirements: dict) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []

    # Capacity: 30 points
    attendees = int(requirements.get("attendees", 150))
    capacity_max = venue.capacity_max

    if capacity_max is not None:
        if capacity_max >= attendees:
            score += 30
            reasons.append("Published capacity meets attendee requirement")
        else:
            reasons.append("Published capacity is below the requirement")
    else:
        reasons.append("Capacity needs confirmation")

    # Budget: 25 points
    budget = requirements.get("budget")
    price = venue.published_price

    if budget is not None and price is not None:
        if price <= budget:
            score += 25
            reasons.append("Published price is within budget")
        else:
            reasons.append("Published price exceeds budget")
    else:
        reasons.append("Final venue cost needs confirmation")

    # Facilities: 40 points total, equally weighted.
    facilities = {
        "wifi": "Wi-Fi",
        "power_outlets": "Power outlets",
        "projector_or_display": "Projector/display",
        "catering": "Catering",
        "parking": "Parking",
    }

    requested = requirements.get("facilities", list(facilities.keys()))
    requested = [field for field in requested if field in facilities]

    if requested:
        points_per_facility = 40 / len(requested)

        for field in requested:
            value = getattr(venue, field)

            if value is True:
                score += points_per_facility
                reasons.append(f"{facilities[field]} is listed")
            elif value is False:
                reasons.append(f"{facilities[field]} is listed as unavailable")
            else:
                reasons.append(f"{facilities[field]} is not verified")

    # The remaining 5 points are reserved for location preference.
    # Don't award them until location matching is implemented.

    return round(min(score, 100), 1), reasons
