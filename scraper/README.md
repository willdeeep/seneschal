# D&D Data Scraper

This directory contains web scraping tools to gather D&D reference data from various sources to populate the Seneschal database.

## Contents

- `requirements.txt` - Dependencies for scraping tools
- `scraper.py` - Main scraping script
- `scrapers/` - Individual scraper modules
- `data/` - Output directory for scraped data
- `config.py` - Configuration settings

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```bash
   python scraper.py
   ```

3. Import data to database:
   ```bash
   python import_data.py
   ```

## Data Sources

- **D&D 5e SRD**: System Reference Document for basic rules
- **D&D Beyond API**: Character options and equipment
- **Open5e**: Open source D&D 5e content

## Legal Notice

This scraper only collects data from publicly available sources and respects robots.txt files. All data scraped is from open content under the Open Gaming License (OGL) or System Reference Document (SRD).
