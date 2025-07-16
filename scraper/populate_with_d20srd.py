#!/usr/bin/env python3
"""
Database population script using D20 SRD scraped data.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project import create_app, db
from project.models import Proficiency, Language, Feature, Item
from scrapers.d20srd import D20SRDScraper
from dnd5e_data import DND5E_PROFICIENCIES, DND5E_FEATURES, DND5E_EQUIPMENT


async def scrape_and_populate_skills():
    """Scrape skills from D20 SRD and populate database."""
    print("Scraping skills from D20 SRD...")
    
    scraper = D20SRDScraper()
    scraped_data = await scraper.scrape_skills()
    
    # Clear existing skill proficiencies
    db.session.query(Proficiency).filter_by(proficiency_type='skills').delete()
    
    added_count = 0
    
    for skill_name, skill_info in scraped_data.items():
        proficiency = Proficiency(
            name=skill_name,
            proficiency_type='skills',
            description=skill_info['description'],
            associated_ability=skill_info['ability']
        )
        db.session.add(proficiency)
        added_count += 1
    
    print(f"Added {added_count} skills from D20 SRD")
    return added_count


def populate_other_proficiencies():
    """Populate non-skill proficiencies from static data."""
    print("Populating other proficiencies...")
    
    # Clear existing non-skill proficiencies
    db.session.query(Proficiency).filter(Proficiency.proficiency_type != 'skills').delete()
    
    added_count = 0
    
    for category, proficiencies in DND5E_PROFICIENCIES.items():
        if category == 'skills':
            continue  # Skip skills, handled by scraper
            
        for prof_name in proficiencies:
            proficiency = Proficiency(
                name=prof_name,
                proficiency_type=category,
                description=f"A {category} proficiency."
            )
            db.session.add(proficiency)
            added_count += 1
    
    print(f"Added {added_count} other proficiencies")
    return added_count


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
        
        language = Language(
            name=language_name,
            language_type=lang_type,
            description=f"The {language_name} language."
        )
        db.session.add(language)
        added_count += 1
    
    print(f"Added {added_count} languages")
    return added_count


def populate_features():
    """Populate database with D&D 5e features."""
    print("Populating features...")
    
    # Clear existing features
    db.session.query(Feature).delete()
    
    added_count = 0
    
    for category, features in DND5E_FEATURES.items():
        for feature_name, feature_desc in features:
            feature = Feature(
                name=feature_name,
                feature_type=category,
                description=feature_desc
            )
            db.session.add(feature)
            added_count += 1
    
    print(f"Added {added_count} features")
    return added_count


def populate_equipment():
    """Populate database with D&D 5e equipment."""
    print("Populating equipment...")
    
    # Clear existing items
    db.session.query(Item).delete()
    
    added_count = 0
    
    for _category, items in DND5E_EQUIPMENT.items():
        for item_name, item_type, cost_gp, weight_lbs, description in items:
            item = Item(
                name=item_name,
                item_type=item_type,
                cost_gp=cost_gp,
                weight_lbs=weight_lbs,
                description=description
            )
            db.session.add(item)
            added_count += 1
    
    print(f"Added {added_count} items")
    return added_count


async def main():
    """Main population function with D20 SRD integration."""
    app = create_app()
    
    with app.app_context():
        print("Starting enhanced database population with D20 SRD data...")
        
        # Create all tables
        db.create_all()
        
        # Populate with scraped and static data
        skills_count = await scrape_and_populate_skills()
        other_prof_count = populate_other_proficiencies()
        lang_count = populate_languages()
        feat_count = populate_features()
        item_count = populate_equipment()
        
        # Commit all changes
        db.session.commit()
        
        # Print summary
        total_prof_count = skills_count + other_prof_count
        
        print("\n" + "="*60)
        print("DATABASE POPULATION COMPLETE WITH D20 SRD DATA")
        print("="*60)
        print(f"Skills (from D20 SRD): {skills_count}")
        print(f"Other Proficiencies: {other_prof_count}")
        print(f"Total Proficiencies: {total_prof_count}")
        print(f"Languages: {lang_count}")
        print(f"Features: {feat_count}")
        print(f"Equipment Items: {item_count}")
        print("="*60)
        
        # Verify by querying database
        actual_prof_count = Proficiency.query.count()
        actual_lang_count = Language.query.count()
        actual_feat_count = Feature.query.count()
        actual_item_count = Item.query.count()
        
        print("\nDatabase verification:")
        print(f"Proficiencies in DB: {actual_prof_count}")
        print(f"Languages in DB: {actual_lang_count}")
        print(f"Features in DB: {actual_feat_count}")
        print(f"Items in DB: {actual_item_count}")
        
        # Show sample of skills with abilities
        print("\nSample skills with associated abilities:")
        sample_skills = Proficiency.query.filter_by(proficiency_type='skills').limit(5).all()
        for skill in sample_skills:
            print(f"- {skill.name} ({skill.associated_ability}): {skill.description[:80]}...")


if __name__ == '__main__':
    asyncio.run(main())
