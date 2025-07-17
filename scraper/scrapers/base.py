"""Base scraper class and utilities."""

import asyncio
import aiohttp
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from asyncio_throttle import Throttler
from config import REQUEST_DELAY, MAX_RETRIES, TIMEOUT, USER_AGENT, DATA_DIR


class BaseScraper(ABC):
    """Base class for all D&D data scrapers."""

    def __init__(self, name: str):
        self.name = name
        self.logger = self._setup_logger()
        self.session: Optional[aiohttp.ClientSession] = None
        self.throttler = Throttler(rate_limit=1 / REQUEST_DELAY)

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for this scraper."""
        logger = logging.getLogger(f"scraper.{self.name}")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=TIMEOUT),
            headers={"User-Agent": USER_AGENT},
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def fetch_json(
        self, url: str, retries: int = MAX_RETRIES
    ) -> Optional[Dict[str, Any]]:
        """Fetch JSON data from URL with retry logic."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")

        async with self.throttler:
            for attempt in range(retries + 1):
                try:
                    self.logger.debug(f"Fetching {url} (attempt {attempt + 1})")
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.logger.debug(f"Successfully fetched {url}")
                            return data
                        elif response.status == 429:  # Rate limited
                            wait_time = 2**attempt
                            self.logger.warning(
                                f"Rate limited. Waiting {wait_time}s before retry."
                            )
                            await asyncio.sleep(wait_time)
                        else:
                            self.logger.warning(f"HTTP {response.status} for {url}")

                except aiohttp.ClientError as e:
                    self.logger.warning(f"Request failed for {url}: {e}")
                    if attempt < retries:
                        await asyncio.sleep(2**attempt)

        self.logger.error(f"Failed to fetch {url} after {retries + 1} attempts")
        return None

    def save_data(self, data: List[Dict[str, Any]], filename: str) -> None:
        """Save scraped data to JSON file."""
        os.makedirs(DATA_DIR, exist_ok=True)
        filepath = os.path.join(DATA_DIR, f"{filename}.json")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved {len(data)} items to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save data to {filepath}: {e}")

    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape data from the source. Must be implemented by subclasses."""
        pass


class DataProcessor:
    """Utility class for processing and cleaning scraped data."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""

        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove common markup that might leak through
        text = text.replace("**", "").replace("*", "")

        return text.strip()

    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize names for consistency."""
        if not name:
            return ""

        # Basic normalization
        name = name.strip()
        name = " ".join(word.capitalize() for word in name.split())

        return name

    @staticmethod
    def parse_dice(dice_str: str) -> Dict[str, Any]:
        """Parse dice notation like '1d8' or '2d6+3'."""
        if not dice_str:
            return {}

        # Simple regex for dice notation
        import re

        match = re.match(r"(\d+)d(\d+)(?:\s*([+-])\s*(\d+))?", dice_str.strip())

        if match:
            count, sides, operator, modifier = match.groups()
            result = {"count": int(count), "sides": int(sides), "original": dice_str}

            if operator and modifier:
                mod_value = int(modifier)
                if operator == "-":
                    mod_value = -mod_value
                result["modifier"] = mod_value

            return result

        return {"original": dice_str}


def setup_data_directories():
    """Set up the data directory structure."""
    categories = [
        "races",
        "classes",
        "spells",
        "equipment",
        "backgrounds",
        "feats",
        "skills",
        "languages",
        "conditions",
        "magic_items",
    ]

    for category in categories:
        os.makedirs(os.path.join(DATA_DIR, category), exist_ok=True)
