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

```mermaid
flowchart TD
    U[Event organizer] --> UI[Streamlit dashboard<br/>app.py]
    UI --> R[Event requirements<br/>type, city, date, attendees,<br/>budget, facilities]

    R --> D[Venue discovery<br/>discovery.py]
    D --> S[TinyFish Search API]
    S --> C[Candidate venue URLs]
    F[User-provided official URLs] -. fallback .-> C

    C --> OR[Research orchestrator<br/>research.py]
    OR --> V{Venue website<br/>validated?}
    V -- no --> E[Show research warning<br/>and continue]
    V -- yes --> B[TinyFish browser agent]
    B --> X[Published facts and<br/>source URLs]

    X --> P[Pydantic validation<br/>models.py]
    P --> SC[Transparent scoring<br/>scoring.py]
    R --> SC
    SC --> O[Ranked venue comparison]

    O --> I[Inquiry draft generator<br/>inquiry.py]
    I --> A[User-controlled actions:<br/>website, email, phone]
    O --> J[(Local JSON results<br/>data/venue_results.json)]
```

| Layer | Responsibility | Main files |
|---|---|---|
| Presentation | Collect event requirements, show progress, compare venues, and expose user-controlled contact actions. | `app.py` |
| Discovery | Search for relevant venue websites, remove duplicates, and use supplied URLs if discovery fails. | `src/venuescout/discovery.py` |
| Research | Validate that a candidate is a venue, browse official pages, and request structured evidence-backed facts. | `src/venuescout/research.py`, `tinyfish_client.py` |
| Validation | Normalize data and represent missing facts as `null` or unverified. | `src/venuescout/models.py` |
| Decisioning | Score capacity, published price, and requested amenities with explainable rules. | `src/venuescout/scoring.py` |
| Follow-up | Generate an editable enquiry draft; users choose whether to open a website, email client, or phone dialer. | `src/venuescout/inquiry.py` |
| Storage | Persist the latest successful research results locally for the MVP. | `data/venue_results.json` |

### Design boundaries

- TinyFish is used for discovery and real website navigation; it is not treated as a source of facts by itself.
- Only information published on venue websites should be marked as verified, with supporting URLs retained.
- Missing capacity, prices, amenities, or availability remain unverified rather than inferred.
- The system never automatically sends email, books a venue, or makes payments.

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
