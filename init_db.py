#!/usr/bin/env python3
"""
Enhanced Database Initialization Script
Robust data sourcing strategy for D&D 5e data.
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError
import zipfile
import tempfile
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError

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
            logger.info(
                "Missing %d files in json_backups: %s...",
                len(missing_files), missing_files[:3]
                )
            return False

        logger.info("✅ All required JSON files found in json_backups")
        return True

    def check_repo_data(self):
        """Check if 5e-database-repo exists and has required files."""
        if not self.repo_path.exists():
            logger.info("5e-database-repo directory doesn't exist")
            return False

        # Files are in src/2014/ directory in the new structure
        src_path = self.repo_path / "src" / "2014"
        if not src_path.exists():
            logger.info("5e-database-repo/src/2014 directory doesn't exist")
            return False

        missing_files = []
        for filename in self.required_files:
            file_path = src_path / filename
            if not file_path.exists():
                missing_files.append(filename)

        if missing_files:
            logger.info("Missing %d files in repo/src/2014: %s...", len(missing_files), missing_files[:3])
            return False

        logger.info("✅ All required JSON files found in 5e-database-repo/src/2014")
        return True

    def copy_from_repo(self):
        """Copy files from 5e-database-repo to json_backups and cleanup repo."""
        logger.info("📂 Copying files from 5e-database-repo to json_backups...")

        # Create json_backups directory if it doesn't exist
        self.json_backups_path.mkdir(exist_ok=True)

        # Files are in src/2014/ directory in the new structure
        src_path = self.repo_path / "src" / "2014"
        copied_count = 0

        for filename in self.required_files:
            src_file = src_path / filename
            dest_file = self.json_backups_path / filename

            if src_file.exists():
                shutil.copy2(src_file, dest_file)
                copied_count += 1
                logger.debug("Copied %s", filename)
            else:
                logger.warning("Source file not found: %s", filename)

        logger.info("✅ Copied %d/%d files", copied_count, len(self.required_files))

        # Cleanup repo directory
        logger.info("🧹 Cleaning up 5e-database-repo directory...")
        shutil.rmtree(self.repo_path)
        logger.info("✅ Repository cleanup completed")

        return copied_count == len(self.required_files)

    def download_source_data(self):
        """Download fresh data from GitHub and extract required files."""
        logger.info("🌐 Downloading fresh data from 5e-bits/5e-database...")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            zip_file = temp_path / "5e-database.zip"

            try:
                # Download the repository
                logger.info("Downloading from %s...", self.source_url)
                urlretrieve(self.source_url, zip_file)
                logger.info("✅ Download completed")

                # Extract the zip file
                logger.info("📦 Extracting archive...")
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)

                # Find the extracted directory (it should be 5e-database-main)
                extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
                if not extracted_dirs:
                    raise FileNotFoundError("No directories found in extracted archive")

                extracted_path = extracted_dirs[0]
                # Files are in src/2014/ directory in the new structure
                src_path = extracted_path / "src" / "2014"

                if not src_path.exists():
                    raise FileNotFoundError("src/2014 directory not found in extracted archive")

                # Create json_backups directory
                self.json_backups_path.mkdir(exist_ok=True)

                # Copy required files
                copied_count = 0
                for filename in self.required_files:
                    src_file = src_path / filename
                    dest_file = self.json_backups_path / filename

                    if src_file.exists():
                        shutil.copy2(src_file, dest_file)
                        copied_count += 1
                        logger.debug("Copied %s", filename)
                    else:
                        logger.warning("File not found in download: %s", filename)

                logger.info("✅ Successfully copied %d/%d files", copied_count, len(self.required_files))
                return copied_count == len(self.required_files)

            except (URLError, HTTPError) as e:
                logger.error("❌ Network error during download: %s", e)
                return False
            except zipfile.BadZipFile as e:
                logger.error("❌ Invalid zip file downloaded: %s", e)
                return False
            except FileNotFoundError as e:
                logger.error("❌ Archive structure error: %s", e)
                return False
            except (OSError, IOError) as e:
                logger.error("❌ File system error during extraction: %s", e)
                return False

    def ensure_data_available(self):
        """Execute complete data sourcing strategy with cascading fallbacks."""
        logger.info("🔍 Executing data sourcing strategy...")

        # Primary: Check json_backups folder
        if self.check_json_backups():
            logger.info("📁 Using existing json_backups data")
            return True

        # Secondary: Check repo folder, copy to json_backups, delete repo
        logger.info("📦 Checking for existing 5e-database-repo...")
        if self.check_repo_data():
            if self.copy_from_repo():
                logger.info("📁 Successfully prepared data from existing repo")
                return True
            else:
                logger.warning("⚠️  Copy from repo failed, continuing to download...")

        # Tertiary: Download fresh from GitHub
        logger.info("🌐 No local data found, downloading fresh data...")
        if self.download_source_data():
            logger.info("🎉 Successfully downloaded and prepared fresh data")
            return True

        # All strategies failed
        logger.error("❌ All data sourcing strategies failed!")
        logger.error("💡 Manual steps:")
        logger.error("   1. Check internet connection")
        logger.error("   2. Manually download: https://github.com/5e-bits/5e-database")
        logger.error("   3. Extract and copy src/*.json files to json_backups/")
        return False

class DatabaseInitializer:
    """Handles database initialization with user prompts and data population."""

    def __init__(self):
        self.data_loader = FiveEDataLoader()

    def check_database_exists(self):
        """Check if database already has data."""
        try:
            species_count = Species.query.count()
            class_count = CharacterClass.query.count()

            if species_count > 0 or class_count > 0:
                logger.info("📊 Existing data found: %d species, %d classes", species_count, class_count)
                return True

            logger.info("📊 Database is empty")
            return False
        except (SQLAlchemyError, OperationalError) as e:
            logger.debug("Database connectivity check failed (normal for first run): %s", e)
            return False

    def create_tables(self):
        """Initialize database schema."""
        logger.info("🏗️  Creating database tables...")
        db.create_all()
        logger.info("✅ Database tables created successfully")

    def populate_species(self):
        """Load species data with terminology mapping."""
        logger.info("🧬 Loading species data...")

        species_data = self.data_loader.get_species()
        if not species_data:
            logger.error("❌ No species data available")
            return False

        loaded_count = 0
        for species_info in species_data:
            try:
                # Parse ability score increases
                ability_increases = {}
                for bonus in species_info.get('ability_bonuses', []):
                    ability_name = bonus.get('ability_score', {}).get('index', '')
                    bonus_value = bonus.get('bonus', 0)
                    if ability_name and bonus_value:
                        ability_increases[ability_name] = bonus_value

                # Parse traits from various sources
                traits = []
                if 'traits' in species_info:
                    traits.extend([trait.get('name', '') for trait in species_info['traits']])

                # Parse languages
                languages = []
                if 'languages' in species_info:
                    languages.extend([lang.get('name', '') for lang in species_info['languages']])

                # Parse proficiencies
                proficiencies = []
                if 'starting_proficiencies' in species_info:
                    proficiencies.extend([prof.get('name', '') for prof in species_info['starting_proficiencies']])

                # Create Species instance
                species = Species(
                    name=species_info.get('name', ''),
                    ability_score_increases=ability_increases,
                    traits=traits,
                    languages=languages,
                    proficiencies=proficiencies,
                    speed=species_info.get('speed', 30),
                    size=species_info.get('size', 'Medium'),
                    source='5e-SRD',
                    description=species_info.get('age', '') + ' ' + species_info.get('alignment', '')
                )

                db.session.add(species)
                loaded_count += 1
                logger.debug("Loaded species: %s", species.name)

            except (KeyError, ValueError, TypeError) as e:
                logger.warning("Data parsing error for species %s: %s", species_info.get('name', 'unknown'), e)

        try:
            db.session.commit()
            logger.info("✅ Successfully loaded %d species", loaded_count)
            return True
        except (SQLAlchemyError, IntegrityError) as e:
            db.session.rollback()
            logger.error("❌ Database error committing species data: %s", e)
            return False

    def populate_classes(self):
        """Load character class data."""
        logger.info("⚔️  Loading character class data...")

        class_data = self.data_loader.get_classes()
        if not class_data:
            logger.error("❌ No character class data available")
            return False

        loaded_count = 0
        for class_info in class_data:
            try:
                # Parse saving throws
                saving_throws = []
                if 'saving_throws' in class_info:
                    saving_throws = [save.get('name', '') for save in class_info['saving_throws']]

                # Parse skill proficiencies from proficiency_choices
                available_skills = []
                skill_choices = 2  # default

                if 'proficiency_choices' in class_info:
                    for choice in class_info['proficiency_choices']:
                        if choice.get('type') == 'proficiencies':
                            skill_choices = choice.get('choose', 2)
                            options = choice.get('from', {}).get('options', [])
                            for option in options:
                                item = option.get('item', {})
                                skill_name = item.get('name', '')
                                if 'Skill:' in skill_name:
                                    available_skills.append(skill_name.replace('Skill: ', ''))

                # Parse proficiencies
                armor_profs = []
                weapon_profs = []

                if 'proficiencies' in class_info:
                    for prof in class_info['proficiencies']:
                        prof_name = prof.get('name', '')
                        if 'Armor' in prof_name:
                            armor_profs.append(prof_name)
                        elif 'Weapon' in prof_name or 'weapons' in prof_name.lower():
                            weapon_profs.append(prof_name)

                # Determine primary ability and spellcasting
                primary_ability = "Strength"  # default
                spellcasting_ability = None

                # Basic mapping based on class name
                class_name = class_info.get('name', '').lower()
                if class_name in ['wizard', 'warlock']:
                    primary_ability = "Intelligence"
                    spellcasting_ability = "Intelligence"
                elif class_name in ['sorcerer', 'bard']:
                    primary_ability = "Charisma"
                    spellcasting_ability = "Charisma"
                elif class_name in ['cleric', 'druid', 'ranger']:
                    primary_ability = "Wisdom"
                    spellcasting_ability = "Wisdom"
                elif class_name in ['rogue', 'ranger']:
                    primary_ability = "Dexterity"
                elif class_name in ['barbarian', 'fighter', 'paladin']:
                    primary_ability = "Strength"
                elif class_name in ['monk']:
                    primary_ability = "Dexterity"
                    spellcasting_ability = "Wisdom"

                # Create CharacterClass instance
                char_class = CharacterClass(
                    name=class_info.get('name', ''),
                    hit_die=class_info.get('hit_die', 8),
                    primary_ability=primary_ability,
                    saving_throw_proficiencies=saving_throws,
                    skill_proficiencies=available_skills,
                    armor_proficiencies=armor_profs,
                    weapon_proficiencies=weapon_profs,
                    skill_choices=skill_choices,
                    spellcasting_ability=spellcasting_ability,
                    source='5e-SRD'
                )

                db.session.add(char_class)
                loaded_count += 1
                logger.debug("Loaded class: %s", char_class.name)

            except (KeyError, ValueError, TypeError) as e:
                logger.warning(
                    "Data parsing error for class %s: %s", class_info.get('name', 'unknown'), e
                    )

        try:
            db.session.commit()
            logger.info("✅ Successfully loaded %d character classes", loaded_count)
            return True
        except (SQLAlchemyError, IntegrityError) as e:
            db.session.rollback()
            logger.error("❌ Database error committing class data: %s", e)
            return False

    def initialize_database(self, force_rebuild=False):
        """Complete database initialization process."""
        logger.info("🎲 Starting database initialization...")

        # Create tables
        self.create_tables()

        # Check for existing data
        if not force_rebuild and self.check_database_exists():
            response = input(
                "\n⚠️  Database already contains data. Rebuild? [y/N]: "
                ).lower().strip()
            if response not in ['y', 'yes']:
                logger.info("⏭️  Skipping database population (existing data preserved)")
                return True

        # Clear existing data if rebuilding
        if self.check_database_exists():
            logger.info("🧹 Clearing existing database data...")
            try:
                # Clear in order of dependencies
                CharacterClass.query.delete()
                Species.query.delete()
                db.session.commit()
                logger.info("✅ Existing data cleared")
            except (SQLAlchemyError, IntegrityError) as e:
                db.session.rollback()
                logger.error("❌ Database error clearing existing data: %s", e)
                return False

        # Populate database
        success = True

        if not self.populate_species():
            success = False

        if not self.populate_classes():
            success = False

        if success:
            logger.info("🎉 Database initialization completed successfully!")
        else:
            logger.error("❌ Database initialization completed with errors")

        return success

def main():
    """Main initialization function with robust data sourcing."""
    logger.info("🎲 D&D 5e Database Initialization")
    logger.info("=" * 50)

    # Step 1: Ensure data is available
    data_manager = DataSourceManager()
    if not data_manager.ensure_data_available():
        logger.error("💥 Cannot proceed without data files")
        sys.exit(1)

    # Step 2: Initialize Flask app context
    app = create_app()

    with app.app_context():
        # Step 3: Initialize database
        db_initializer = DatabaseInitializer()

        # Check command line arguments for force rebuild
        force_rebuild = '--force' in sys.argv or '-f' in sys.argv

        if db_initializer.initialize_database(force_rebuild=force_rebuild):
            logger.info("🎉 Initialization completed successfully!")

            # Show summary
            species_count = Species.query.count()
            class_count = CharacterClass.query.count()
            logger.info("📊 Final counts: %d species, %d classes", species_count, class_count)
        else:
            logger.error("💥 Initialization failed!")
            sys.exit(1)

if __name__ == "__main__":
    main()
