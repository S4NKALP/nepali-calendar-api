# Nepali Calendar Data

Machine-readable Nepali calendar dataset and scraper covering 1992 BS to the present.

## Features

- Accurate Nepali (BS) to English (AD) date mapping
- Detailed Tithi information
- Religious festivals and public holidays
- Auspicious monthly dates for Marriage and Bratabandha
- Automated scraper for continuous data updates

## Data Structure

The dataset is organized in the `data/` directory and is available in two formats:

1. **Aggregated Yearly Data**: `data/<year>.json`
   - A single JSON file containing all 12 months for a specific year.
2. **Individual Monthly Data**: `data/<year>/<month>.json`
   - Modular files for granular data access.

## Scraper Usage

The repository includes a Python-based scraper that uses `uv` for dependency management and performance.

### Prerequisites

Ensure you have `uv` installed on your system.

### Basic Commands

Generate data for a single year or a range (produces both formats by default):

```bash
uv run scraper.py 2082
uv run scraper.py 2077 2085
```

### Advanced Configuration

Use flags to control the output format:

- **Generate Single JSON only**:
  ```bash
  uv run scraper.py 2082 --single json
  ```

- **Generate Directory Format (Monthly Files) only**:
  ```bash
  uv run scraper.py 2082 --dir format
  ```

## API Server

The repository includes a FastAPI-based server to serve the scrapped data.

### Running the API

```bash
uv run uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- `GET /calendar/{year}`: Returns the aggregated yearly calendar data.
- `GET /calendar/{year}/{month}`: Returns the individual monthly calendar data.
- `GET /docs`: Interactive API documentation (Swagger UI).

## Maintenance

This repository is actively maintained. New calendar data is added as it becomes available.
