# Nepali Calendar Data API

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0+-009688.svg)](https://fastapi.tiangolo.com/)
[![Built with uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Leapcell Deployment](https://img.shields.io/badge/Deploy-Leapcell-000?style=flat&logo=leapcell)](https://api-nepalicalendar.leapcell.app)

A machine-readable Nepali calendar (Bikram Sambat) dataset and high-performance API. This project provides automated scraping, structured data storage, and a RESTful interface for calendar data from 1992 BS to the present.

---

## 🚀 Live API

The API is deployed and publicly accessible:  
**[https://api-nepalicalendar.leapcell.app](https://api-nepalicalendar.leapcell.app)**

Interactive documentation (Swagger UI) is available at:  
**[/docs](https://api-nepalicalendar.leapcell.app/docs)**

---

## ✨ Features

- **Accurate Mapping**: Reliable BS to AD date conversion.
- **Rich Metadata**: Includes Tithi, religious festivals, and public holidays.
- **Auspicious Dates**: Monthly data for Marriage and Bratabandha.
- **Dual Format Storage**: Optimized for both bulk (yearly) and granular (monthly) access.
- **High Performance**: Built with FastAPI and `uv` for minimal overhead.
- **Zero-Touch Updates**: Automated daily scraping via GitHub Actions with dynamic year calculation.

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.13+**
- **[uv](https://github.com/astral-sh/uv)** (highly recommended for dependency management)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/S4NKALP/nepali-calendar-api.git
   cd nepali-calendar-api
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Running the API Locally

```bash
uv run uvicorn app:app --reload
```
The server will start at `http://localhost:8000`.

---

## 📊 Data Structure

Dataset resides in the `/data` directory:

- **Aggregated Yearly**: `data/<year>.json` (Full 12-month payload)
- **Modular Monthly**: `data/<year>/<month>.json` (Lightweight monthly payload)

### Sample Output Format

```json
{
  "metadata": {
    "np": "बैशाख २०८२",
    "en": "Apr/May 2025"
  },
  "days": [
    {
      "d": 2,
      "n": "१",
      "e": "14",
      "t": "प्रतिपदा",
      "f": "navavarsha 2082",
      "h": true
    }
  ],
  "holiFest": ["navavarsha 2082..."],
  "marriage": ["..."],
  "bratabandha": ["..."]
}
```

---

## 🕵️ Scraper Usage

The scraper is the core engine for dataset expansion.

```bash
# Scrape specific year
uv run scraper.py 2082

# Scrape range
uv run scraper.py 2070 2085

# Format-specific flags
uv run scraper.py 2082 --single json   # Aggregated only
uv run scraper.py 2082 --dir format    # Monthly files only
```

---

## 🤖 CI/CD & Automation

This project uses **GitHub Actions** (`.github/workflows/scrape.yml`) to keep the data fresh.
- **Frequency**: Runs daily at 00:00 UTC.
- **Intelligence**: Automatically calculates the current BS year and updates folders.
- **Manual Control**: Supports `workflow_dispatch` to manually scrape any year via the GitHub UI.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

