#!/usr/bin/env python3
"""
Enhanced database population script using curated D&D 5e data.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project import create_app, db
from project.models import Proficiency, Language, Feature, Item
from dnd5e_data import DND5E_PROFICIENCIES, DND5E_FEATURES, DND5E_EQUIPMENT


def populate_proficiencies():
    """Populate database with D&D 5e proficiencies."""
    print("Populating proficiencies...")
    
    # Clear existing proficiencies
    db.session.query(Proficiency).delete()
    
    added_count = 0
    
    for category, proficiencies in DND5E_PROFICIENCIES.items():
        for prof_name in proficiencies:
            # Check if proficiency already exists
            existing = Proficiency.query.filter_by(name=prof_name).first()
            if not existing:
                proficiency = Proficiency(
                    name=prof_name,
                    proficiency_type=category,
                    description=f"A {category} proficiency."
                )
                db.session.add(proficiency)
                added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} proficiencies")


def populate_languages():
    """Populate database with D&D 5e languages."""
    print("Populating languages...")
    
    # Clear existing languages
    db.session.query(Language).delete()
    
    added_count = 0
    
    for language_name in DND5E_PROFICIENCIES['languages']:
        # Determine language type
        common_languages = ['Common', 'Dwarvish', 'Elvish', 'Giant', 'Gnomish', 'Goblin', 'Halfling', 'Orc']
        exotic_languages = ['Abyssal', 'Celestial', 'Draconic', 'Deep Speech', 'Infernal', 'Primordial', 'Sylvan', 'Undercommon']
        
        if language_name in common_languages:
            lang_type = 'Standard'
        elif language_name in exotic_languages:
            lang_type = 'Exotic'
        else:
            lang_type = 'Dialect'
        
        # Check if language already exists
        existing = Language.query.filter_by(name=language_name).first()
        if not existing:
            language = Language(
                name=language_name,
                language_type=lang_type,
                description=f"The {language_name} language."
            )
            db.session.add(language)
            added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} languages")


def populate_features():
    """Populate database with D&D 5e features."""
    print("Populating features...")
    
    # Clear existing features
    db.session.query(Feature).delete()
    
    added_count = 0
    
    for category, features in DND5E_FEATURES.items():
        for feature_name, feature_desc in features:
            # Check if feature already exists
            existing = Feature.query.filter_by(name=feature_name).first()
            if not existing:
                feature = Feature(
                    name=feature_name,
                    feature_type=category,
                    description=feature_desc
                )
                db.session.add(feature)
                added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} features")


def populate_equipment():
    """Populate database with D&D 5e equipment."""
    print("Populating equipment...")
    
    # Clear existing items
    db.session.query(Item).delete()
    
    added_count = 0
    
    for _category, items in DND5E_EQUIPMENT.items():
        for item_name, item_type, cost_gp, weight_lbs, description in items:
            # Check if item already exists
            existing = Item.query.filter_by(name=item_name).first()
            if not existing:
                item = Item(
                    name=item_name,
                    item_type=item_type,
                    cost_gp=cost_gp,
                    weight_lbs=weight_lbs,
                    description=description
                )
                db.session.add(item)
                added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} items")


def main():
    """Main population function."""
    app = create_app()
    
    with app.app_context():
        print("Starting enhanced database population...")
        
        # Create all tables
        db.create_all()
        
        # Populate with comprehensive D&D data
        populate_proficiencies()
        populate_languages()
        populate_features()
        populate_equipment()
        
        # Print summary
        prof_count = Proficiency.query.count()
        lang_count = Language.query.count()
        feat_count = Feature.query.count()
        item_count = Item.query.count()
        
        print("\n" + "="*50)
        print("DATABASE POPULATION COMPLETE")
        print("="*50)
        print(f"Total Proficiencies: {prof_count}")
        print(f"Total Languages: {lang_count}")
        print(f"Total Features: {feat_count}")
        print(f"Total Items: {item_count}")
        print("="*50)


if __name__ == '__main__':
    main()
