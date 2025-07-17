#!/usr/bin/env python3
"""
Database population script using D20 SRD scraped data and enhanced models.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project import create_app, db
from project.models import Proficiency, Language, Feature, Item, Spell
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


async def scrape_and_populate_spells():
    """Scrape spells from D20 SRD and populate database."""
    print("Scraping spells from D20 SRD...")

    scraper = D20SRDScraper()
    scraped_data = await scraper.scrape_spells()

    # Clear existing spells
    db.session.query(Spell).delete()

    added_count = 0

    # Basic spell data from scraper - we'll enhance with manual data later
    for spell_name, spell_info in scraped_data.items():
        # Skip very short names that are likely navigation elements
        if len(spell_name) < 3 or spell_name.lower() in ['aid', 'wish']:
            continue
            
        spell = Spell(
            name=spell_name,
            level=spell_info.get('level', 1),
            school=spell_info.get('school', 'unknown'),
            description=f"A {spell_info.get('school', 'unknown')} spell.",
            casting_time="1 action",  # Default values
            spell_range="Touch",
            components="V, S",
            duration="Instantaneous",
            is_ritual=False,
            requires_concentration=False
        )
        db.session.add(spell)
        added_count += 1

    print(f"Added {added_count} spells from D20 SRD")
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
                description=f"Proficiency with {prof_name}."
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
            description=f"The {language_name} language spoken by various creatures and cultures."
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
            # Determine usage patterns based on feature name
            uses_per_rest = None
            rest_type = None
            
            if 'once per' in feature_desc.lower():
                if 'short' in feature_desc.lower():
                    uses_per_rest = 1
                    rest_type = 'short'
                elif 'long' in feature_desc.lower():
                    uses_per_rest = 1
                    rest_type = 'long'
            
            feature = Feature(
                name=feature_name,
                feature_type=category,
                description=feature_desc,
                uses_per_rest=uses_per_rest,
                rest_type=rest_type
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
        for item_data in items:
            item_name, item_type, cost_gp, weight_lbs, description = item_data
            
            # Enhanced item creation with weapon/armor properties
            item = Item(
                name=item_name,
                item_type=item_type,
                cost_gp=cost_gp,
                weight_lbs=weight_lbs,
                description=description
            )
            
            # Add weapon-specific properties
            if item_type == 'weapon':
                item = enhance_weapon_properties(item, item_name)
            
            # Add armor-specific properties
            elif item_type == 'armor':
                item = enhance_armor_properties(item, item_name)
            
            db.session.add(item)
            added_count += 1

    print(f"Added {added_count} items")
    return added_count


def enhance_weapon_properties(item, weapon_name):
    """Add weapon-specific properties based on weapon name."""
    weapon_data = {
        'Dagger': {'damage_dice': '1d4', 'damage_type': 'piercing', 'weapon_properties': 'finesse, light, thrown (range 20/60)'},
        'Shortsword': {'damage_dice': '1d6', 'damage_type': 'piercing', 'weapon_properties': 'finesse, light'},
        'Longsword': {'damage_dice': '1d8', 'damage_type': 'slashing', 'weapon_properties': 'versatile (1d10)'},
        'Rapier': {'damage_dice': '1d8', 'damage_type': 'piercing', 'weapon_properties': 'finesse'},
        'Scimitar': {'damage_dice': '1d6', 'damage_type': 'slashing', 'weapon_properties': 'finesse, light'},
        'Greataxe': {'damage_dice': '1d12', 'damage_type': 'slashing', 'weapon_properties': 'heavy, two-handed'},
        'Greatsword': {'damage_dice': '2d6', 'damage_type': 'slashing', 'weapon_properties': 'heavy, two-handed'},
        'Battleaxe': {'damage_dice': '1d8', 'damage_type': 'slashing', 'weapon_properties': 'versatile (1d10)'},
        'Warhammer': {'damage_dice': '1d8', 'damage_type': 'bludgeoning', 'weapon_properties': 'versatile (1d10)'},
        'Shortbow': {'damage_dice': '1d6', 'damage_type': 'piercing', 'weapon_properties': 'ammunition (range 80/320), two-handed'},
        'Longbow': {'damage_dice': '1d8', 'damage_type': 'piercing', 'weapon_properties': 'ammunition (range 150/600), heavy, two-handed'},
        'Light Crossbow': {'damage_dice': '1d8', 'damage_type': 'piercing', 'weapon_properties': 'ammunition (range 80/320), loading, two-handed'},
        'Heavy Crossbow': {'damage_dice': '1d10', 'damage_type': 'piercing', 'weapon_properties': 'ammunition (range 100/400), heavy, loading, two-handed'},
    }

    if weapon_name in weapon_data:
        data = weapon_data[weapon_name]
        item.damage_dice = data.get('damage_dice')
        item.damage_type = data.get('damage_type')
        item.weapon_properties = data.get('weapon_properties')
        
        # Set weapon range
        if 'ranged' in data.get('weapon_properties', '').lower() or 'bow' in weapon_name.lower():
            item.weapon_range = 'ranged'
        else:
            item.weapon_range = 'melee'

    return item


def enhance_armor_properties(item, armor_name):
    """Add armor-specific properties based on armor name."""
    armor_data = {
        'Leather Armor': {'armor_class': 11, 'max_dex_bonus': None, 'stealth_disadvantage': False},
        'Studded Leather': {'armor_class': 12, 'max_dex_bonus': None, 'stealth_disadvantage': False},
        'Hide Armor': {'armor_class': 12, 'max_dex_bonus': 2, 'stealth_disadvantage': False},
        'Chain Shirt': {'armor_class': 13, 'max_dex_bonus': 2, 'stealth_disadvantage': False},
        'Scale Mail': {'armor_class': 14, 'max_dex_bonus': 2, 'stealth_disadvantage': True},
        'Breastplate': {'armor_class': 14, 'max_dex_bonus': 2, 'stealth_disadvantage': False},
        'Half Plate': {'armor_class': 15, 'max_dex_bonus': 2, 'stealth_disadvantage': True},
        'Ring Mail': {'armor_class': 14, 'max_dex_bonus': 0, 'stealth_disadvantage': True},
        'Chain Mail': {'armor_class': 16, 'max_dex_bonus': 0, 'stealth_disadvantage': True, 'min_strength': 13},
        'Splint Armor': {'armor_class': 17, 'max_dex_bonus': 0, 'stealth_disadvantage': True, 'min_strength': 15},
        'Plate Armor': {'armor_class': 18, 'max_dex_bonus': 0, 'stealth_disadvantage': True, 'min_strength': 15},
        'Shield': {'armor_class': 2, 'max_dex_bonus': None, 'stealth_disadvantage': False},
    }

    if armor_name in armor_data:
        data = armor_data[armor_name]
        item.armor_class = data.get('armor_class')
        item.max_dex_bonus = data.get('max_dex_bonus')
        item.stealth_disadvantage = data.get('stealth_disadvantage', False)
        item.min_strength = data.get('min_strength')

    return item


async def main():
    """Main population function with D20 SRD integration."""
    app = create_app()

    with app.app_context():
        print("Starting enhanced database population with D20 SRD data...")
        print("="*60)
        
        # Create all tables
        db.create_all()
        
        # Populate with scraped and static data
        skills_count = await scrape_and_populate_skills()
        spells_count = await scrape_and_populate_spells()
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
        print(f"Spells (from D20 SRD): {spells_count}")
        print(f"Other Proficiencies: {other_prof_count}")
        print(f"Total Proficiencies: {total_prof_count}")
        print(f"Languages: {lang_count}")
        print(f"Features: {feat_count}")
        print(f"Equipment Items: {item_count}")
        print("="*60)
        
        # Verify by querying database
        actual_prof_count = Proficiency.query.count()
        actual_spell_count = Spell.query.count()
        actual_lang_count = Language.query.count()
        actual_feat_count = Feature.query.count()
        actual_item_count = Item.query.count()
        
        print("\nDatabase verification:")
        print(f"Proficiencies in DB: {actual_prof_count}")
        print(f"Spells in DB: {actual_spell_count}")
        print(f"Languages in DB: {actual_lang_count}")
        print(f"Features in DB: {actual_feat_count}")
        print(f"Items in DB: {actual_item_count}")
        
        # Show sample of skills with abilities
        print("\nSample skills with associated abilities:")
        sample_skills = Proficiency.query.filter_by(proficiency_type='skills').limit(5).all()
        for skill in sample_skills:
            print(f"- {skill.name} ({skill.associated_ability}): {skill.description[:80]}...")
        
        # Show sample spells
        print("\nSample spells:")
        sample_spells = Spell.query.limit(5).all()
        for spell in sample_spells:
            print(f"- {spell.name} (Level {spell.level}, {spell.school})")
        
        # Show sample enhanced weapons
        print("\nSample weapons with properties:")
        sample_weapons = Item.query.filter_by(item_type='weapon').filter(Item.damage_dice.isnot(None)).limit(3).all()
        for weapon in sample_weapons:
            print(f"- {weapon.name}: {weapon.damage_dice} {weapon.damage_type}, {weapon.weapon_properties}")


if __name__ == '__main__':
    asyncio.run(main())
