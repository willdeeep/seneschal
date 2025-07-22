#!/usr/bin/env python3
"""
Enhanced Database Initialization Script
Robust data sourcing strategy for D&D 5e data.
"""

import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path
from urllib.request import urlretrieve
import zipfile
import tempfile

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from project import create_app, db
from project.models import Species, CharacterClass
from json_data_loader import FiveEDataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataSourceManager:
    """Manages the robust data sourcing strategy."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.json_backups_path = self.base_path / "json_backups"
        self.repo_path = self.base_path / "5e-database-repo"
        self.source_url = "https://github.com/5e-bits/5e-database/archive/refs/heads/main.zip"
        
        # Required JSON files for database initialization
        self.required_files = [
            "5e-SRD-Races.json",
            "5e-SRD-Classes.json",
            "5e-SRD-Spells.json",
            "5e-SRD-Equipment.json",
            "5e-SRD-Monsters.json",
            "5e-SRD-Skills.json",
            "5e-SRD-Backgrounds.json",
            "5e-SRD-Features.json",
            "5e-SRD-Proficiencies.json",
            "5e-SRD-Languages.json"
        ]
    
    def check_json_backups(self):
        """Check if all required JSON files exist in json_backups."""
        if not self.json_backups_path.exists():
            logger.info("json_backups directory doesn't exist")
            return False
        
        missing_files = []
        for filename in self.required_files:
            file_path = self.json_backups_path / filename
            if not file_path.exists():
                missing_files.append(filename)
        
        if missing_files:
            logger.info(f"Missing {len(missing_files)} files in json_backups: {missing_files[:3]}...")
            return False
        
        logger.info("✅ All required JSON files found in json_backups")
        return True

def main():
    """Main initialization function."""
    logger.info("🎲 D&D 5e Database Initialization")
    logger.info("=" * 50)
    
    # Initialize Flask app context
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        logger.info("✅ Database tables created successfully")
        
        # Load data using JSON loader
        data_loader = FiveEDataLoader()
        
        # Test data loading
        species_data = data_loader.get_species()
        class_data = data_loader.get_classes()
        
        logger.info(f"📊 Found {len(species_data)} species and {len(class_data)} classes")
        logger.info("🎉 Basic initialization completed!")

if __name__ == "__main__":
    main()
