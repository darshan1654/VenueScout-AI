# VenueScout AI

VenueScout AI is a Streamlit application that helps event organizers discover,
research, and compare venues. It uses TinyFish browser automation to inspect
official venue websites and shows only published, source-backed information.

## The problem

Venue research is usually a manual process: searching for options, visiting
many websites, comparing incomplete capacity and amenity information, then
emailing venues for prices and availability. VenueScout AI creates a structured
shortlist while marking unsupported facts as unverified.

The application recommends venues; it does not make bookings, send email, or
guarantee availability.

## Features

- Event requirements form for event type, city, attendees, budget, date, and facilities.
- Candidate discovery with TinyFish Search and a user-provided URL fallback.
- Website research with TinyFish and Pydantic-validated venue records.
- Transparent rule-based scoring for capacity, published price, and facilities.
- Evidence URLs and explicit unknown-field warnings.
- An editable enquiry draft plus direct website, email, and phone actions when public contact details are available.

## Architecture

```text
Streamlit form -> candidate discovery -> TinyFish website research
    -> Pydantic validation -> rule-based scoring -> comparison and enquiry actions
```

## Setup

1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the following template:

   ```env
   TINYFISH_API_KEY=your_key_here
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Testing

Run the offline unit tests with:

```bash
python -m pytest -q
```

## Limitations

- Research quality depends on each venue's public website.
- Published prices and availability are often incomplete; those fields remain unverified until confirmed with the venue.
- The MVP ranks venues using a simple, explainable scoring system and currently does not score travel time or date availability.
- Website, email, and phone actions always require the user's final action.

## Security

Never commit `.env` or API keys. The supplied `.gitignore` excludes local
secrets, virtual environments, and generated Python cache files.
