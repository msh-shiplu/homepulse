# HomePulse — Real Estate MLS & Public Disclosure Explorer

Live App: **[https://msh-shiplu.github.io/homepulse/](https://msh-shiplu.github.io/homepulse/)**

HomePulse is a real estate due-diligence and property discovery platform that traverses **Redfin MLS For-Sale feeds**, **Zillow / Redfin Rental feeds**, **OpenStreetMap Nominatim / Overpass parcels**, and **FEMA National Flood Hazard Layer (NFHL)** records.

## Key Features

- **Zero API Keys Required for Maps & Geocoding**:
  - Interactive radius & pin maps powered by **Leaflet** with 4 switchable tile layers (**Street**, **Esri Aerial Satellite**, **Topographic**, and **Dark Mode**).
  - Live address, neighborhood, city, and ZIP code autocomplete & geocoding via **OpenStreetMap Nominatim**.
  - Exact **Haversine distance** filtering (`1` to `50` miles) with interactive radius circles and `"Search This Map Area"` pan/zoom detection.
- **Real Property Feeds (Redfin MLS & Zillow Rentals)**:
  - Automated `scraper.py` + GitHub Actions workflow (`.github/workflows/scrape_listings.yml`) traverses **1,270+ active For-Sale & For-Rent homes** across **18 major US metro areas** (`data/listings.json`).
  - Multi-photo high-resolution MLS & rental photo carousels on every property card and disclosure modal.
  - Direct 1-click verification links to **Redfin**, **Zillow**, **Realtor.com**, and **Google Street View**.
- **Public Disclosures, Hazard Audit & Objective Pros/Cons**:
  - **Live FEMA NFHL Flood Zone Check**: Queries FEMA's official ArcGIS REST API (`hazards.fema.gov`) on the fly when inspecting any property.
  - **Objective Pros & Cons**: Grounded in each parcel's real `yearBuilt` (pre-1978 lead paint / plumbing / electrical code eras), `$/sqft` vs. local metro median, HOA dues, Days on Market (`dom`), and MLS key facts.
  - **Built-in Property Inspector**: Instant physical inspection checklists, rental yield / cap-rate math, 5-year resale risk, and offer negotiation strategies without requiring an LLM API key (with optional Gemini 2.5 Flash support).

## Running Locally with Live On-Demand Feed Traversal

```bash
# Refresh the 18-metro dataset (data/listings.json)
python3 scraper.py

# Start the local web server + live on-demand /api/traverse proxy
python3 server.py
```