#!/usr/bin/env python3
"""
5e JSON Data Loader
Utilities for loading and accessing D&D 5e data from JSON files.
"""

import json
from pathlib import Path
import logging

class FiveEDataLoader:
    """Load and access D&D 5e data from JSON files."""

    def __init__(self, data_path=None):
        """Initialize data loader with path to JSON files."""
        if data_path is None:
            data_path = Path(__file__).parent / "json_backups"

        self.data_path = Path(data_path)
        self.logger = logging.getLogger(__name__)
        self._cache = {}

    def load_json_file(self, filename):
        """Load and parse a JSON file with caching."""
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.data_path / filename

        if not file_path.exists():
            self.logger.error("File not found: %s", file_path)
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._cache[filename] = data
            record_count = len(data) if isinstance(data, list) else 1
            self.logger.info("Loaded %d records from %s", record_count, filename)
            return data
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error("Error loading %s: %s", filename, e)
            return []

    def get_species(self):
        """Get species (races) data."""
        return self.load_json_file("5e-SRD-Races.json")

    def get_classes(self):
        """Get character classes data."""
        return self.load_json_file("5e-SRD-Classes.json")

# Global instance for easy access
data_loader = FiveEDataLoader()
