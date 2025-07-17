#!/usr/bin/env python3
"""
Debug script for validating Character model functionality.
This script is specifically designed for debugging character creation,
validation, and relationship handling.
"""

import os
import sys
from flask import Flask
from sqlalchemy import text

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from project import create_app, db
from project.models import (
    Character, User, Proficiency, Language, Feature, 
    Item, CharacterItem, Spell, SpellSlot
)


def debug_character_creation():
    """Debug character creation with comprehensive validation."""
    print("🎯 Starting Character Model Debug Session")
    print("=" * 50)

    app = create_app()

    with app.app_context():
        # Test database connection
        try:
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return
        
        # Create a test user if none exists
        test_user = User.query.filter_by(email='debug@test.com').first()
        if not test_user:
            test_user = User(
                email='debug@test.com',
                name='Debug User'
            )
            test_user.set_password('debug123')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Created debug user")
        else:
            print("ℹ️  Using existing debug user")
        
        # Test character creation with enhanced backstory fields
        print("\n🎲 Testing Character Creation")
        print("-" * 30)
        
        # Create a test character
        test_character = Character(
            name="Debug Warrior",
            player_name="Debug Player",
            race="Human",
            subrace="Variant Human",
            character_class="Fighter",
            subclass="Champion",
            level=3,
            background="Soldier",
            alignment="Lawful Good",
            
            # Core stats
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
            
            # Combat stats
            max_hp=28,
            current_hp=28,
            armor_class=18,
            initiative=2,
            
            # Enhanced backstory fields
            why_adventuring="Seeking to prove honor after a military disgrace",
            motivation="Honor, redemption, protecting the innocent",
            origin="Born in a small military outpost on the frontier",
            class_origin="Trained as a soldier from a young age, natural fighter",
            attachments="Old military unit, younger sister back home",
            secret="Was blamed for a tactical error that wasn't his fault",
            attitude_origin="Stoic and duty-bound due to military upbringing",
            
            # Currency
            gold_pieces=150,
            silver_pieces=50,
            
            # Relationships
            user_id=test_user.id
        )
        
        # Test saving throws
        test_character.str_save_proficient = True
        test_character.con_save_proficient = True
        
        try:
            db.session.add(test_character)
            db.session.commit()
            print(f"✅ Character created: {test_character.name} (ID: {test_character.id})")
            
            # Test ability modifier calculations
            print(f"   STR modifier: {test_character.get_ability_modifier(test_character.strength)}")
            print(f"   DEX modifier: {test_character.get_ability_modifier(test_character.dexterity)}")
            
            # Test saving throw calculations
            str_save = test_character.get_saving_throw_bonus('strength')
            dex_save = test_character.get_saving_throw_bonus('dexterity')
            print(f"   STR save: +{str_save} (proficient)")
            print(f"   DEX save: +{dex_save} (not proficient)")
            
            # Test proficiency bonus update
            original_bonus = test_character.proficiency_bonus
            test_character.level = 5
            test_character.update_proficiency_bonus()
            print(f"   Proficiency bonus updated: {original_bonus} → {test_character.proficiency_bonus}")
            
        except Exception as e:
            print(f"❌ Character creation failed: {e}")
            db.session.rollback()
            return
        
        # Test backstory field validation
        print("\n📖 Testing Backstory Fields")
        print("-" * 30)
        backstory_fields = [
            'why_adventuring', 'motivation', 'origin', 'class_origin',
            'attachments', 'secret', 'attitude_origin'
        ]
        
        for field in backstory_fields:
            value = getattr(test_character, field)
            if value:
                print(f"✅ {field}: {value[:50]}{'...' if len(value) > 50 else ''}")
            else:
                print(f"⚠️  {field}: Not set")
        
        # Test relationships
        print("\n🔗 Testing Relationships")
        print("-" * 30)
        
        # Test adding proficiencies
        skill_proficiencies = Proficiency.query.filter_by(proficiency_type='skill').limit(3).all()
        if skill_proficiencies:
            for prof in skill_proficiencies:
                if prof not in test_character.proficiencies:
                    test_character.proficiencies.append(prof)
            db.session.commit()
            print(f"✅ Added {len(skill_proficiencies)} skill proficiencies")
        
        # Test adding languages
        languages = Language.query.limit(2).all()
        if languages:
            for lang in languages:
                if lang not in test_character.languages:
                    test_character.languages.append(lang)
            db.session.commit()
            print(f"✅ Added {len(languages)} languages")
        
        # Test spell slots (for testing purposes)
        print("\n🎭 Testing Spell Slots")
        print("-" * 30)
        
        # Add some spell slots
        spell_slot_1 = SpellSlot(
            character_id=test_character.id,
            level=1,
            total_slots=2,
            used_slots=0
        )
        spell_slot_2 = SpellSlot(
            character_id=test_character.id,
            level=2,
            total_slots=1,
            used_slots=1
        )
        
        db.session.add_all([spell_slot_1, spell_slot_2])
        db.session.commit()
        
        print(f"✅ Level 1 slots: {spell_slot_1.remaining_slots}/{spell_slot_1.total_slots}")
        print(f"✅ Level 2 slots: {spell_slot_2.remaining_slots}/{spell_slot_2.total_slots}")
        
        # Test spell slot usage
        if spell_slot_1.use_slot():
            print("✅ Used a level 1 spell slot")
        
        spell_slot_1.long_rest()
        print("✅ Restored all slots after long rest")
        
        # Summary
        print("\n📊 Debug Summary")
        print("-" * 30)
        print(f"Character: {test_character.name}")
        print(f"Level: {test_character.level}")
        print(f"Class: {test_character.character_class}")
        print(f"Race: {test_character.race}")
        print(f"HP: {test_character.current_hp}/{test_character.max_hp}")
        print(f"AC: {test_character.armor_class}")
        print(f"Proficiencies: {len(test_character.proficiencies)}")
        print(f"Languages: {len(test_character.languages)}")
        print(f"Spell Slots: {len(test_character.spell_slots)}")
        print(f"Backstory fields populated: {sum(1 for field in backstory_fields if getattr(test_character, field))}/{len(backstory_fields)}")
        
        print("\n🎯 Debug session completed successfully!")


def debug_database_queries():
    """Debug common database queries."""
    print("\n🔍 Testing Database Queries")
    print("-" * 30)

    app = create_app()

    with app.app_context():
        # Test character queries
        characters = Character.query.all()
        print(f"Total characters: {len(characters)}")
        
        # Test relationship queries
        if characters:
            char = characters[0]
            print(f"Character '{char.name}' has {len(char.proficiencies)} proficiencies")
            print(f"Character '{char.name}' has {len(char.languages)} languages")
            print(f"Character '{char.name}' has {len(char.spell_slots)} spell slot levels")
        
        # Test filtering
        fighters = Character.query.filter_by(character_class='Fighter').all()
        print(f"Fighter characters: {len(fighters)}")
        
        humans = Character.query.filter_by(race='Human').all()
        print(f"Human characters: {len(humans)}")


if __name__ == "__main__":
    print("🚀 Character Model Debug Tool")
    print("This script will test character creation, validation, and relationships.")
    print()

    # Set breakpoint here for debugging
    debug_character_creation()
    debug_database_queries()

    print("\n✨ All debugging completed!")
