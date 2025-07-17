"""Configuration settings for D&D data scraper."""

import os

# Base URLs for data sources
OPEN5E_BASE_URL = "https://api.open5e.com"
DND5E_API_BASE_URL = "https://www.dnd5eapi.co/api"

# Rate limiting settings
REQUEST_DELAY = 1.0  # Delay between requests in seconds
MAX_RETRIES = 3
TIMEOUT = 30

# Output settings
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FORMAT = "json"  # json, csv, yaml

# User agent for requests
USER_AGENT = "Seneschal D&D Character Manager Scraper (Educational/Personal Use)"

# What data to scrape
SCRAPE_CONFIG = {
    "races": True,
    "classes": True,
    "spells": True,
    "equipment": True,
    "monsters": False,  # Not needed for character sheets
    "backgrounds": True,
    "feats": True,
    "skills": True,
    "languages": True,
    "conditions": True,
    "magic_items": True,
}

# Database connection (for direct import)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://seneschal_user:seneschal_password@localhost:5433/seneschal_db",
)

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(os.path.dirname(__file__), "scraper.log")
