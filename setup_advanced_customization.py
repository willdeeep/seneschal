"""Create tables for advanced character customization."""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from project import create_app, db
from project.models import Background, Equipment, User


def create_tables():
    """Create the new tables for advanced character customization."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Tables created successfully!")


def seed_backgrounds():
    """Seed basic D&D 5e backgrounds."""
    app = create_app()
    
    with app.app_context():
        backgrounds_data = [
            {
                "name": "Acolyte",
                "description": "You have spent your life in the service of a temple to a specific god or pantheon.",
                "skill_proficiencies": ["Insight", "Religion"],
                "tool_proficiencies": [],
                "languages": ["Any two languages"],
                "equipment": ["Holy Symbol", "Prayer Book", "Incense", "Vestments", "Common Clothes"],
                "feature_name": "Shelter of the Faithful",
                "feature_description": "You can perform religious ceremonies and receive free healing at temples."
            },
            {
                "name": "Criminal",
                "description": "You are an experienced criminal with a history of breaking the law.",
                "skill_proficiencies": ["Deception", "Stealth"],
                "tool_proficiencies": ["Thieves' Tools", "Gaming Set"],
                "languages": [],
                "equipment": ["Crowbar", "Dark Common Clothes", "Belt Pouch"],
                "feature_name": "Criminal Contact",
                "feature_description": "You have a reliable contact in the criminal underworld."
            },
            {
                "name": "Folk Hero",
                "description": "You come from a humble social rank, but you are destined for so much more.",
                "skill_proficiencies": ["Animal Handling", "Survival"],
                "tool_proficiencies": ["Artisan's Tools", "Vehicles (Land)"],
                "languages": [],
                "equipment": ["Artisan's Tools", "Shovel", "Iron Pot", "Common Clothes"],
                "feature_name": "Rustic Hospitality",
                "feature_description": "Common folk shelter you and hide you from the law or others."
            },
            {
                "name": "Noble",
                "description": "You understand wealth, power, and privilege from birth.",
                "skill_proficiencies": ["History", "Persuasion"],
                "tool_proficiencies": ["Gaming Set"],
                "languages": ["Any one language"],
                "equipment": ["Signet Ring", "Scroll of Pedigree", "Fine Clothes"],
                "feature_name": "Position of Privilege",
                "feature_description": "You are welcome in high society and can arrange meetings with nobles."
            },
            {
                "name": "Sage",
                "description": "You spent years learning the lore of the multiverse.",
                "skill_proficiencies": ["Arcana", "History"],
                "tool_proficiencies": [],
                "languages": ["Any two languages"],
                "equipment": ["Ink", "Quill", "Small Knife", "Scroll Case", "Common Clothes"],
                "feature_name": "Researcher",
                "feature_description": "You know how to obtain information and can recall lore."
            },
            {
                "name": "Soldier",
                "description": "You have a military background and experience with warfare.",
                "skill_proficiencies": ["Athletics", "Intimidation"],
                "tool_proficiencies": ["Gaming Set", "Vehicles (Land)"],
                "languages": [],
                "equipment": ["Insignia of Rank", "Trophy", "Playing Cards", "Common Clothes"],
                "feature_name": "Military Rank",
                "feature_description": "Your rank grants you authority over soldiers and access to military facilities."
            }
        ]

        for bg_data in backgrounds_data:
            existing = Background.query.filter_by(name=bg_data["name"]).first()
            if not existing:
                background = Background(**bg_data)
                db.session.add(background)

        db.session.commit()
        print("Backgrounds seeded successfully!")


def seed_equipment():
    """Seed basic D&D 5e equipment."""
    app = create_app()
    
    with app.app_context():
        equipment_data = [
            # Weapons
            {"name": "Dagger", "category": "Weapon", "cost_cp": 200, "weight": 1.0, 
             "damage_dice": "1d4", "damage_type": "Piercing", "weapon_properties": ["Finesse", "Light", "Thrown"]},
            {"name": "Shortsword", "category": "Weapon", "cost_cp": 1000, "weight": 2.0,
             "damage_dice": "1d6", "damage_type": "Piercing", "weapon_properties": ["Finesse", "Light"]},
            {"name": "Rapier", "category": "Weapon", "cost_cp": 2500, "weight": 2.0,
             "damage_dice": "1d8", "damage_type": "Piercing", "weapon_properties": ["Finesse"]},
            {"name": "Longsword", "category": "Weapon", "cost_cp": 1500, "weight": 3.0,
             "damage_dice": "1d8", "damage_type": "Slashing", "weapon_properties": ["Versatile"]},
            {"name": "Handaxe", "category": "Weapon", "cost_cp": 500, "weight": 2.0,
             "damage_dice": "1d6", "damage_type": "Slashing", "weapon_properties": ["Light", "Thrown"]},
            {"name": "Light Crossbow", "category": "Weapon", "cost_cp": 2500, "weight": 5.0,
             "damage_dice": "1d8", "damage_type": "Piercing", "weapon_properties": ["Ammunition", "Loading", "Two-Handed"]},
            {"name": "Quarterstaff", "category": "Weapon", "cost_cp": 20, "weight": 4.0,
             "damage_dice": "1d6", "damage_type": "Bludgeoning", "weapon_properties": ["Versatile"]},
            
            # Armor
            {"name": "Leather Armor", "category": "Armor", "cost_cp": 1000, "weight": 10.0,
             "armor_class": 11, "max_dex_bonus": None, "stealth_disadvantage": False},
            {"name": "Chain Mail", "category": "Armor", "cost_cp": 7500, "weight": 55.0,
             "armor_class": 16, "max_dex_bonus": 0, "min_strength": 13, "stealth_disadvantage": True},
            {"name": "Scale Mail", "category": "Armor", "cost_cp": 5000, "weight": 45.0,
             "armor_class": 14, "max_dex_bonus": 2, "stealth_disadvantage": True},
            {"name": "Shield", "category": "Armor", "cost_cp": 1000, "weight": 6.0,
             "armor_class": 2, "description": "+2 AC when wielded"},
            
            # Tools
            {"name": "Thieves' Tools", "category": "Tool", "cost_cp": 2500, "weight": 1.0,
             "description": "Includes lockpicks and other tools for thievery"},
            {"name": "Component Pouch", "category": "Tool", "cost_cp": 2500, "weight": 2.0,
             "description": "Contains material components for spellcasting"},
            
            # Equipment Packs
            {"name": "Explorer's Pack", "category": "Equipment Pack", "cost_cp": 1000, "weight": 10.0,
             "description": "Includes backpack, bedroll, mess kit, tinderbox, 10 torches, 10 days of rations, waterskin, 50 feet of hempen rope"},
            {"name": "Burglar's Pack", "category": "Equipment Pack", "cost_cp": 1600, "weight": 12.0,
             "description": "Includes backpack, bag of 1,000 ball bearings, 10 feet of string, bell, 5 candles, crowbar, hammer, 10 pitons, hooded lantern, 2 flasks of oil, 5 days rations, tinderbox, waterskin, 50 feet of hempen rope"},
            {"name": "Scholar's Pack", "category": "Equipment Pack", "cost_cp": 4000, "weight": 10.0,
             "description": "Includes backpack, book of lore, bottle of ink, ink pen, 10 sheets of parchment, little bag of sand, small knife"},
            {"name": "Priest's Pack", "category": "Equipment Pack", "cost_cp": 1900, "weight": 12.0,
             "description": "Includes backpack, blanket, 10 candles, tinderbox, alms box, 2 blocks of incense, censer, vestments, 2 days of rations, waterskin"},
            
            # Miscellaneous
            {"name": "Spellbook", "category": "Spellcasting Focus", "cost_cp": 5000, "weight": 3.0,
             "description": "Required for wizards to prepare and cast spells"},
            {"name": "Holy Symbol", "category": "Spellcasting Focus", "cost_cp": 500, "weight": 1.0,
             "description": "Used by clerics and paladins as a spellcasting focus"},
        ]

        for eq_data in equipment_data:
            existing = Equipment.query.filter_by(name=eq_data["name"]).first()
            if not existing:
                equipment = Equipment(**eq_data)
                db.session.add(equipment)

        db.session.commit()
        print("Equipment seeded successfully!")


def create_test_user():
    """Create a test user for API testing and development."""
    app = create_app()
    
    with app.app_context():
        # Check if test user already exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            print("Test user already exists!")
            return

        # Create test user
        test_user = User(
            name='Test User',
            email='test@example.com'
        )
        test_user.set_password('testpass123')

        db.session.add(test_user)
        db.session.commit()

        print("Test user created successfully!")
        print("  Name: Test User")
        print("  Email: test@example.com") 
        print("  Password: testpass123")


if __name__ == "__main__":
    create_tables()
    seed_backgrounds()
    seed_equipment()
    create_test_user()
    print("Advanced character customization setup complete!")
