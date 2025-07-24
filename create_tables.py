#!/usr/bin/env python3
"""Create database tables and populate with D&D data."""

from init_db import DataSourceManager, DatabaseInitializer
from project.models import (
    User,
    Character,
    Proficiency,
    Language,
    Feature,
    Item,
    CharacterItem,
    Species,
    CharacterClass,
)
from project import create_app, db
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, "/app")


def create_tables():
    """Create all database tables."""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        print("Initializing D&D data...")

        # Ensure data sources are available
        data_manager = DataSourceManager()
        if not data_manager.ensure_data_available():
            print("Error: Cannot proceed without data files")
            return False

        # Initialize database with D&D data
        db_initializer = DatabaseInitializer()
        success = db_initializer.initialize_database(force_rebuild=False)

        if success:
            print("Database tables created and D&D data initialized successfully!")

            # Print summary
            try:
                print(f"Users: {User.query.count()}")
                print(f"Characters: {Character.query.count()}")
                print(f"Species: {Species.query.count()}")
                print(f"Character Classes: {CharacterClass.query.count()}")
                print(f"Proficiencies: {Proficiency.query.count()}")
                print(f"Languages: {Language.query.count()}")
                print(f"Features: {Feature.query.count()}")
                print(f"Items: {Item.query.count()}")
            except Exception as e:
                print(f"Warning: Could not retrieve counts: {e}")

            return True
        else:
            print("Error: Database initialization failed")
            return False


if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
