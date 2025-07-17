"""Database initialization script to populate D&D data."""

from project import create_app, db
from project.models import Proficiency, Language, Feature, Item


def init_proficiencies():
    """Initialize basic D&D proficiencies."""
    proficiencies = [
        # Skills
        ("Acrobatics", "skill"),
        ("Animal Handling", "skill"),
        ("Arcana", "skill"),
        ("Athletics", "skill"),
        ("Deception", "skill"),
        ("History", "skill"),
        ("Insight", "skill"),
        ("Intimidation", "skill"),
        ("Investigation", "skill"),
        ("Medicine", "skill"),
        ("Nature", "skill"),
        ("Perception", "skill"),
        ("Performance", "skill"),
        ("Persuasion", "skill"),
        ("Religion", "skill"),
        ("Sleight of Hand", "skill"),
        ("Stealth", "skill"),
        ("Survival", "skill"),
        # Weapons
        ("Simple Weapons", "weapon"),
        ("Martial Weapons", "weapon"),
        ("Shortswords", "weapon"),
        ("Longswords", "weapon"),
        ("Rapiers", "weapon"),
        ("Scimitars", "weapon"),
        ("Shortbows", "weapon"),
        ("Longbows", "weapon"),
        ("Light Crossbows", "weapon"),
        ("Hand Crossbows", "weapon"),
        # Armor
        ("Light Armor", "armor"),
        ("Medium Armor", "armor"),
        ("Heavy Armor", "armor"),
        ("Shields", "armor"),
        # Tools
        ("Thieves' Tools", "tool"),
        ("Herbalism Kit", "tool"),
        ("Smith's Tools", "tool"),
        ("Carpenter's Tools", "tool"),
        ("Alchemist's Supplies", "tool"),
        ("Disguise Kit", "tool"),
        ("Forgery Kit", "tool"),
        ("Gaming Set", "tool"),
        ("Musical Instrument", "tool"),
    ]

    for name, prof_type in proficiencies:
        if not Proficiency.query.filter_by(name=name).first():
            proficiency = Proficiency(name=name, proficiency_type=prof_type)
            db.session.add(proficiency)


def init_languages():
    """Initialize basic D&D languages."""
    languages = [
        "Common",
        "Dwarvish",
        "Elvish",
        "Giant",
        "Gnomish",
        "Goblin",
        "Halfling",
        "Orc",
        "Abyssal",
        "Celestial",
        "Draconic",
        "Deep Speech",
        "Infernal",
        "Primordial",
        "Sylvan",
        "Undercommon",
    ]

    for name in languages:
        if not Language.query.filter_by(name=name).first():
            language = Language(name=name)
            db.session.add(language)


def init_features():
    """Initialize basic D&D features."""
    features = [
        # Racial Features
        (
            "Darkvision",
            "You can see in dim light within 60 feet of you as if it were bright light.",
            "Race",
        ),
        (
            "Fey Ancestry",
            "You have advantage on saving throws against being charmed, and magic cannot put you to sleep.",
            "Race",
        ),
        (
            "Lucky",
            "When you roll a 1 on an attack roll, ability check, or saving throw, you can reroll the die.",
            "Race",
        ),
        (
            "Brave",
            "You have advantage on saving throws against being frightened.",
            "Race",
        ),
        (
            "Halfling Nimbleness",
            "You can move through the space of any creature that is of a size larger than yours.",
            "Race",
        ),
        (
            "Draconic Ancestry",
            "You have draconic ancestry. Choose one type of dragon from the table.",
            "Race",
        ),
        (
            "Breath Weapon",
            "You can use your action to exhale destructive energy.",
            "Race",
        ),
        (
            "Damage Resistance",
            "You have resistance to the damage type associated with your draconic ancestry.",
            "Race",
        ),
        # Class Features
        ("Rage", "In battle, you fight with primal ferocity.", "Class"),
        (
            "Unarmored Defense",
            "While you are not wearing any armor, your AC equals 10 + your Dex modifier.",
            "Class",
        ),
        (
            "Bardic Inspiration",
            "You can inspire others through stirring words or music.",
            "Class",
        ),
        (
            "Spellcasting",
            "You have learned to untangle and reshape the fabric of reality.",
            "Class",
        ),
        (
            "Channel Divinity",
            "You gain the ability to channel divine energy directly from your deity.",
            "Class",
        ),
        (
            "Wild Shape",
            "You can use your action to magically assume the shape of a beast.",
            "Class",
        ),
        (
            "Fighting Style",
            "You adopt a particular style of fighting as your specialty.",
            "Class",
        ),
        (
            "Second Wind",
            "You have a limited well of stamina that you can draw on.",
            "Class",
        ),
        (
            "Action Surge",
            "You can push yourself beyond your normal limits for a moment.",
            "Class",
        ),
        (
            "Martial Arts",
            "You gain the following benefits while you are unarmed or wielding only monk weapons.",
            "Class",
        ),
        ("Ki", "Your training allows you to harness the mystic energy of ki.", "Class"),
        (
            "Divine Sense",
            "You can detect the presence of strong evil or good.",
            "Class",
        ),
        ("Lay on Hands", "Your blessed touch can heal wounds.", "Class"),
        (
            "Favored Enemy",
            "You have studied, tracked, and learned to effectively fight a specific type of creature.",
            "Class",
        ),
        (
            "Natural Explorer",
            "You are particularly familiar with one type of natural environment.",
            "Class",
        ),
        (
            "Sneak Attack",
            "You know how to strike subtly and exploit a foe's distraction.",
            "Class",
        ),
        (
            "Thieves' Cant",
            "You know thieves' cant, a secret mix of dialect, jargon, and code.",
            "Class",
        ),
        (
            "Sorcerous Origin",
            "Choose a sorcerous origin, which describes the source of your innate magical power.",
            "Class",
        ),
        (
            "Font of Magic",
            "At 2nd level, you tap into a deep wellspring of magic within yourself.",
            "Class",
        ),
        (
            "Otherworldly Patron",
            "You have struck a pact with an otherworldly being.",
            "Class",
        ),
        (
            "Pact Magic",
            "Your arcane research and the magic bestowed on you by your patron have given you facility with spells.",
            "Class",
        ),
        (
            "Arcane Recovery",
            "You have learned to regain some of your magical energy by studying your spellbook.",
            "Class",
        ),
        (
            "Ritual Casting",
            "You can cast a spell as a ritual if that spell has the ritual tag.",
            "Class",
        ),
    ]

    for name, description, source in features:
        if not Feature.query.filter_by(name=name).first():
            # Map source to feature_type
            feature_type_map = {
                "Race": "racial",
                "Class": "class",
                "Background": "background",
            }
            feature_type = feature_type_map.get(source, "general")

            # Set source_class for class features
            source_class = None
            if source == "Class":
                source_class = "General"  # Could be enhanced to specify actual classes

            feature = Feature(
                name=name,
                description=description,
                feature_type=feature_type,
                source_class=source_class,
            )
            db.session.add(feature)


def init_items():
    """Initialize basic D&D equipment."""
    items = [
        # Weapons
        ("Longsword", "weapon", 15, 3.0, "A versatile martial weapon."),
        ("Shortsword", "weapon", 10, 2.0, "A light, finesse weapon."),
        ("Dagger", "weapon", 2, 1.0, "A simple weapon that can be thrown."),
        ("Handaxe", "weapon", 5, 2.0, "A light weapon that can be thrown."),
        ("Javelin", "weapon", 5, 2.0, "A thrown weapon."),
        ("Mace", "weapon", 5, 4.0, "A simple melee weapon."),
        ("Rapier", "weapon", 25, 2.0, "A finesse weapon."),
        ("Scimitar", "weapon", 25, 3.0, "A finesse, light weapon."),
        ("Shortbow", "weapon", 25, 2.0, "A ranged weapon."),
        ("Longbow", "weapon", 50, 2.0, "A ranged weapon with longer range."),
        ("Light Crossbow", "weapon", 25, 5.0, "A ranged weapon."),
        # Armor
        (
            "Leather Armor",
            "armor",
            10,
            10.0,
            "Light armor made of supple and thin materials.",
        ),
        ("Studded Leather", "armor", 45, 13.0, "Light armor with metal studs."),
        (
            "Chain Shirt",
            "armor",
            50,
            20.0,
            "Medium armor made of interlocking metal rings.",
        ),
        (
            "Scale Mail",
            "armor",
            50,
            45.0,
            "Medium armor consisting of a coat and leggings.",
        ),
        (
            "Chain Mail",
            "armor",
            75,
            55.0,
            "Heavy armor made of interlocking metal rings.",
        ),
        (
            "Splint Armor",
            "armor",
            200,
            60.0,
            "Heavy armor made of narrow vertical strips.",
        ),
        (
            "Plate Armor",
            "armor",
            1500,
            65.0,
            "Heavy armor consisting of shaped metal plates.",
        ),
        ("Shield", "armor", 10, 6.0, "A shield made from wood or metal."),
        # Adventuring Gear
        ("Backpack", "gear", 2, 5.0, "A leather pack carried on the back."),
        ("Bedroll", "gear", 1, 7.0, "A sleeping bag and blanket."),
        ("Blanket", "gear", 5, 3.0, "A thick quilt for warmth."),
        ("Rope (50 feet)", "gear", 2, 10.0, "Hempen rope."),
        ("Torch", "gear", 1, 1.0, "A torch burns for 1 hour."),
        (
            "Rations (1 day)",
            "consumable",
            2,
            2.0,
            "Dry foods suitable for extended travel.",
        ),
        ("Waterskin", "gear", 2, 5.0, "A waterskin can hold 4 pints of liquid."),
        (
            "Thieves' Tools",
            "tool",
            25,
            1.0,
            "Tools for picking locks and disarming traps.",
        ),
        (
            "Healer's Kit",
            "tool",
            5,
            3.0,
            "A kit with bandages, splints, and other supplies.",
        ),
        (
            "Tinderbox",
            "gear",
            5,
            1.0,
            "A small container holding flint, fire steel, and tinder.",
        ),
        ("Lantern", "gear", 5, 2.0, "A hooded lantern casts bright light."),
        ("Oil (flask)", "consumable", 1, 1.0, "Oil usually comes in a clay flask."),
        (
            "Potion of Healing",
            "consumable",
            50,
            0.5,
            "A magic potion that restores hit points.",
        ),
        # Tools
        ("Smith's Tools", "tool", 20, 8.0, "Tools for working with metal."),
        ("Carpenter's Tools", "tool", 8, 6.0, "Tools for working with wood."),
        (
            "Alchemist's Supplies",
            "tool",
            50,
            8.0,
            "Equipment for creating alchemical items.",
        ),
        ("Herbalism Kit", "tool", 5, 3.0, "Tools for identifying and using herbs."),
        ("Disguise Kit", "tool", 25, 3.0, "Cosmetics, hair dye, and props."),
        ("Forgery Kit", "tool", 15, 5.0, "Paper, inks, and other supplies."),
    ]

    for name, item_type, cost, weight, description in items:
        if not Item.query.filter_by(name=name).first():
            item = Item(
                name=name,
                item_type=item_type,
                cost_gp=cost,
                weight_lbs=weight,
                description=description,
            )
            db.session.add(item)


def init_db():
    """Initialize the database with basic D&D data."""
    app = create_app()

    with app.app_context():
        # Create tables
        db.create_all()

        # Initialize data
        print("Initializing proficiencies...")
        init_proficiencies()

        print("Initializing languages...")
        init_languages()

        print("Initializing features...")
        init_features()

        print("Initializing items...")
        init_items()

        # Commit all changes
        try:
            db.session.commit()
            print("Database initialization completed successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")


if __name__ == "__main__":
    init_db()
