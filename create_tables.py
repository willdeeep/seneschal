#!/usr/bin/env python3
"""Create database tables and populate with D&D data."""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, '/app')

from project import create_app, db
from project.models import User, Character, Proficiency, Language, Feature, Item, CharacterItem
from init_db import init_proficiencies, init_languages, init_features, init_items


def create_tables():
    """Create all database tables."""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Initializing D&D data...")
        
        # Initialize reference data
        init_proficiencies()
        init_languages()
        init_features() 
        init_items()
        
        try:
            db.session.commit()
            print("Database tables created and D&D data initialized successfully!")
            
            # Print summary
            print(f"Proficiencies: {Proficiency.query.count()}")
            print(f"Languages: {Language.query.count()}")
            print(f"Features: {Feature.query.count()}")
            print(f"Items: {Item.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return False
            
        return True


if __name__ == '__main__':
    success = create_tables()
    sys.exit(0 if success else 1)
