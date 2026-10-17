# VenueScout AI — Project Plan

## 1. Project Overview

**Project Name:** VenueScout AI  
**Category:** AI Agents | Browser Automation | Event Planning  
**Core Platform:** TinyFish Agent API  
**Target:** 4–5 hour hackathon MVP

VenueScout AI is an AI-powered venue research and comparison assistant that helps event organizers discover suitable venues, research their websites, compare facilities and prices, and prepare venue inquiry messages in one place.

The initial use case is finding a venue for a hackathon in Bengaluru, India. The system should be designed to support other events, including seminars, conferences, workshops, corporate events, weddings, and private celebrations.

## 2. Problem Statement

Finding the right venue is a time-consuming manual process. Event organizers often need to:

- Search Google Maps, search engines, and venue directories.
- Open multiple venue websites.
- Find information about capacity, facilities, pricing, and location.
- Contact venues individually to ask about availability and quotations.
- Compare options manually in spreadsheets or notes.

Information is often scattered across websites, and prices or availability may not be published.

VenueScout AI aims to reduce this effort by automating venue discovery, website research, information extraction, and comparison.

## 3. Proposed Solution

The user enters their event requirements. VenueScout AI discovers potential venues, uses TinyFish to navigate their real websites, extracts published information, and presents a comparison of the most suitable options.

The application should clearly distinguish verified website information from missing or unconfirmed details.

**Primary objective:** Help users create a research-backed shortlist of suitable venues without visiting every website manually.

The application recommends venues; it does not guarantee availability or automatically book them.

## 4. Initial Demo Scenario

The first version will focus on the following example:

- **Event:** AI/technology hackathon
- **Location:** Bengaluru, Karnataka, India
- **Expected attendees:** 150
- **Duration:** One day
- **Maximum venue budget:** ₹1,00,000
- **Required facilities:**
  - Reliable Wi-Fi
  - Sufficient power outlets for participants
  - Projector or display equipment
  - Food and catering options
  - Parking facilities

These values are initial demo defaults. Users should be able to modify them through the application.

## 5. Core Features

### Feature 1: Event Requirement Form

Allow users to enter:

- Event type
- City or preferred area
- Event date
- Number of attendees
- Event duration
- Maximum budget
- Required facilities
- Optional preferences, such as parking, accessibility, or proximity to public transport

### Feature 2: Hybrid Venue Discovery

Find candidate venues using a discovery source, such as a search API, venue directory, or places API.

The discovery process should:

1. Search for venues relevant to the event type and city.
2. Collect venue names, website URLs, and available location details.
3. Remove duplicate candidates.
4. Prioritize candidates with useful official websites.
5. Use a small curated fallback list if automated discovery fails.

The discovery provider finds candidate venues; TinyFish performs the deeper website research.

Do not rely on unauthorized scraping of Google Maps. Use permitted APIs or other suitable discovery sources.

### Feature 3: TinyFish Website Research

TinyFish is the central execution and research component of VenueScout AI.

For each candidate venue, the agent should:

1. Open the venue website.
2. Navigate relevant pages, such as facilities, event spaces, pricing, and contact pages.
3. Extract information explicitly published by the venue.
4. Return structured results that Python can validate.
5. Preserve source URLs and evidence for extracted facts.
6. Report missing information instead of inventing values.

Research fields include:

- Venue name
- Official website
- Address and area
- Published event capacity
- Published rental price or pricing information
- Wi-Fi availability
- Power outlets or charging facilities
- Projector or display equipment
- Catering or food options
- Parking
- Public contact details
- Event-date availability, if explicitly published

If pricing requires a quotation or availability needs confirmation, mark it accordingly.

### Feature 4: Data Validation and Normalization

Use Python and Pydantic to convert the collected information into a consistent structure.

Requirements:

- Normalize field names and data types.
- Handle incomplete or malformed responses.
- Preserve source URLs.
- Avoid duplicate venue records.
- Represent unavailable information as `null`, `unknown`, or `not verified`.
- Distinguish published prices from estimates and quotations.
- Never treat unverified information as a confirmed fact.

### Feature 5: Venue Comparison and Ranking

Compare venues against the user's requirements.

Possible scoring criteria:

- Capacity suitability
- Budget compatibility
- Required facilities
- Location preference
- Completeness of published information

Use a transparent, rule-based scoring formula for the MVP.

Hard requirements, such as minimum capacity and maximum budget, should be treated separately from preferences. A venue should not receive a high score merely because its website omits important information.

Explain why each venue received its score and identify unmet or unverified requirements.

### Feature 6: Streamlit Dashboard

Build a simple web interface using Streamlit.

The dashboard should include:

- Event requirements form
- Start-research button
- Research progress and status
- Shortlisted venue cards or comparison table
- Published prices and available facilities
- Match scores and reasons
- Official website and evidence links
- Missing-information warnings
- Contact details when publicly available

The interface should be clear, responsive, and suitable for a live hackathon demonstration.

### Feature 7: Venue Inquiry Assistant

Generate a customized inquiry message for each shortlisted venue.

The draft should ask about:

- Availability on the requested date
- Total rental cost, including taxes and deposits
- Capacity and seating arrangements
- Wi-Fi and power availability
- Audio-visual equipment
- Catering options
- Parking
- Additional charges and venue restrictions

The user reviews and sends the message manually. Automated email or WhatsApp sending is outside the initial MVP.

## 6. System Architecture

The proposed architecture is:

```text
User
 |
 v
Streamlit Interface
 |
 v
Event Requirements
 |
 v
Venue Discovery Module
(Search API / Directory / Curated Fallback)
 |
 v
Candidate Venue URLs
 |
 v
TinyFish Agent API
(Real Website Navigation and Research)
 |
 v
Structured Research Results
 |
 v
Python + Pydantic Validation
 |
 v
Requirement-Based Scoring
 |
 +----------------------+
 |                      |
 v                      v
Venue Comparison     Inquiry Draft
 |                      |
 +-----------+----------+
             |
             v
      Streamlit Results
```

TinyFish must be central to the workflow by carrying out real website navigation and research, rather than merely returning static or manually prepared information.

## 7. Recommended Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Main application logic |
| Website research | TinyFish Agent API | Navigate real venue websites |
| User interface | Streamlit | Event form and comparison dashboard |
| Data validation | Pydantic | Validate and normalize results |
| API requests | Requests or HTTPX | Communicate with external APIs |
| Environment variables | python-dotenv | Load API keys securely |
| Venue discovery | Search or places API | Find candidate venues |
| Data storage | JSON | Store MVP results |
| Version control | Git and GitHub | Track and share the project |

An additional LLM may be used for extraction assistance or inquiry drafting if needed. Avoid adding unnecessary services before the core workflow works.

## 8. Proposed Project Structure

```text
VenueScout-AI/
|
|-- app.py
|-- plan.md
|-- README.md
|-- requirements.txt
|-- .env
|-- .gitignore
|
|-- src/
|   |-- venuescout/
|       |-- __init__.py
|       |-- tinyfish_client.py
|       |-- discovery.py
|       |-- research.py
|       |-- models.py
|       |-- scoring.py
|       |-- inquiry.py
|       |-- utils.py
|
|-- data/
|   |-- .gitkeep
|
|-- tests/
|   |-- test_models.py
|   |-- test_scoring.py
|
|-- screenshots/
    |-- .gitkeep
```

### File responsibilities

- `app.py`: Streamlit application and user interface.
- `plan.md`: Project plan and implementation roadmap.
- `README.md`: Project overview, installation, architecture, and usage.
- `requirements.txt`: Python dependencies.
- `.env`: Local API keys; never commit this file.
- `.gitignore`: Exclude secrets, virtual environments, caches, and generated files.
- `tinyfish_client.py`: TinyFish API requests and streaming response handling.
- `discovery.py`: Search for candidate venues and normalize discovery results.
- `research.py`: Orchestrate TinyFish research for candidate venue websites.
- `models.py`: Pydantic data models for venue information.
- `scoring.py`: Requirement checks and venue ranking.
- `inquiry.py`: Generate venue inquiry drafts.
- `utils.py`: Shared helpers and data-processing functions.
- `data/`: Local generated results where needed.
- `tests/`: Tests for data validation and scoring.
- `screenshots/`: Screenshots for the README and final presentation.

The structure can be simplified if necessary to meet the hackathon deadline.

## 9. Time-Boxed Implementation Plan

### Phase 1 — Setup and API Verification (0–30 minutes)

- Confirm the Python virtual environment works.
- Verify the TinyFish API key is loaded from `.env`.
- Keep the working TinyFish smoke test.
- Confirm the project does not expose secrets in Git.

**Deliverable:** A successful TinyFish request.

### Phase 2 — Venue Website Research (30–90 minutes)

- Implement the reusable TinyFish client.
- Research one real venue website.
- Extract a small set of fields.
- Return structured results.
- Handle errors and missing data.

**Deliverable:** One venue research result with source evidence.

### Phase 3 — Hybrid Discovery (90–135 minutes)

- Implement the discovery module.
- Find a small set of potential Bengaluru venues.
- Normalize and deduplicate candidate URLs.
- Add a curated fallback list.
- Limit the initial research run to approximately 3–5 venues.

**Deliverable:** A list of candidate venues ready for TinyFish research.

### Phase 4 — Validation and Scoring (135–180 minutes)

- Implement the venue data model.
- Normalize results.
- Check capacity, budget, and facilities.
- Calculate a transparent match score.
- Flag unknown information.

**Deliverable:** A validated, ranked venue shortlist.

### Phase 5 — Dashboard and Inquiry Drafts (180–240 minutes)

- Build the Streamlit requirements form.
- Add the research button and progress status.
- Display comparison results and source links.
- Add the inquiry draft generator.

**Deliverable:** A usable end-to-end application.

### Phase 6 — Testing and Presentation (240–300 minutes)

- Test successful and failed website research.
- Verify that missing data is handled correctly.
- Check the shortlist against the event requirements.
- Capture screenshots.
- Prepare a short demonstration and explain the architecture.

**Deliverable:** A reliable MVP and a clear hackathon presentation.

**Priority rule:** If time is running short, prioritize one working end-to-end workflow over adding more features.

## 10. MVP Acceptance Criteria

The MVP is ready to demonstrate when:

- [ ] The user can enter event requirements.
- [ ] The application discovers candidate venues or uses a clearly identified fallback.
- [ ] TinyFish researches real venue websites.
- [ ] Research results are normalized into structured data.
- [ ] Source URLs are available for researched information.
- [ ] Unknown information is not fabricated.
- [ ] The application compares and ranks venues.
- [ ] The dashboard explains important matches and missing details.
- [ ] The user can generate an inquiry draft.
- [ ] Errors do not crash the entire application.
- [ ] API keys remain private and are excluded from Git.

## 11. Evaluation and Success Metrics

Measure actual results during testing:

- Number of candidate venues discovered.
- Number of venue websites successfully researched.
- Number and percentage of requested fields verified.
- Percentage of populated facts supported by source URLs.
- Time required to research the shortlisted venues.
- Number of venues satisfying the essential requirements.
- Number of website failures handled gracefully.

Compare against a manual research baseline if possible. Do not claim time savings, accuracy improvements, or other performance gains without measurements.

## 12. Risks and Mitigation

### Website access failures

Some websites may block automated navigation or load information dynamically.

**Mitigation:** Retry selectively, record errors, and continue with other candidates.

### Missing or quote-only prices

Many venues do not publish complete pricing.

**Mitigation:** Mark pricing as quote required and generate an inquiry draft.

### Incorrect or outdated information

A website may contain outdated details or incomplete information.

**Mitigation:** Preserve source URLs and advise users to confirm important facts directly.

### Slow research

Multiple websites may take time to process.

**Mitigation:** Limit the initial run to a small number of candidates and show progress.

### Discovery API limitations

An API may require credentials, have usage limits, or restrict certain uses.

**Mitigation:** Check provider documentation and have a curated fallback list ready.

### Hallucinated data

An AI system may infer details that are not published.

**Mitigation:** Validate the output, retain evidence, and leave unsupported fields unknown.

## 13. Security and Responsible Use

- Store API keys in `.env`.
- Never commit credentials to GitHub.
- Respect website terms, access controls, and applicable API rules.
- Collect only relevant public venue information.
- Do not bypass login requirements or access restrictions.
- Do not automatically contact venues, book venues, or make payments.
- Clearly distinguish published facts from unverified information.

## 14. GitHub and Deliverables

The GitHub repository should contain:

- Source code
- `plan.md`
- `README.md`
- `requirements.txt`
- `.gitignore`
- Tests
- Screenshots of the working application

The repository must not contain `.env`, API keys, virtual environment files, or private credentials.

The README should explain the problem, solution, architecture, technology stack, setup instructions, screenshots, demo workflow, and limitations.

### Final deliverables

1. Working VenueScout AI MVP.
2. TinyFish-powered venue research workflow.
3. Venue comparison dashboard.
4. Source-backed venue shortlist.
5. Venue inquiry draft generator.
6. GitHub repository with documentation.
7. Short demo presentation.

## 15. Future Enhancements

After the MVP, potential improvements include:

- Map-based venue exploration.
- Travel-time comparison from a specified landmark.
- More event types and cities.
- Better search and discovery coverage.
- Venue availability and quotation tracking.
- User-approved email integration.
- Saved shortlists and export to CSV/PDF.
- Multi-agent research and cross-source verification.
- Persistent event projects and collaboration.

These features are not required for the initial hackathon version.

## Final Objective

Build a functional, transparent, and useful AI venue research assistant that demonstrates TinyFish navigating real websites to solve a genuine event-planning problem.

**The guiding principle is simple: discover venues, research their real websites, compare evidence-backed facts, and help the user make an informed decision.**
