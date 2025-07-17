from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Association tables for many-to-many relationships
character_proficiencies = db.Table(
    "character_proficiencies",
    db.Column(
        "character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True
    ),
    db.Column(
        "proficiency_id", db.Integer, db.ForeignKey("proficiency.id"), primary_key=True
    ),
)

character_languages = db.Table(
    "character_languages",
    db.Column(
        "character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True
    ),
    db.Column(
        "language_id", db.Integer, db.ForeignKey("language.id"), primary_key=True
    ),
)

character_features = db.Table(
    "character_features",
    db.Column(
        "character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True
    ),
    db.Column("feature_id", db.Integer, db.ForeignKey("feature.id"), primary_key=True),
)

character_spells = db.Table(
    "character_spells",
    db.Column(
        "character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True
    ),
    db.Column("spell_id", db.Integer, db.ForeignKey("spell.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    """User model for authentication and user management."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Relationship to characters
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    characters = db.relationship("Character", backref="owner", lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Character(db.Model):
    """Character model for D&D character sheets."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    player_name = db.Column(db.String(100), nullable=True)
    level = db.Column(db.Integer, default=1, nullable=False)
    background = db.Column(db.String(100), nullable=True)
    alignment = db.Column(db.String(30), nullable=True)  # e.g., "Chaotic Good"

    # Experience and advancement
    experience_points = db.Column(db.Integer, default=0, nullable=False)
    proficiency_bonus = db.Column(
        db.Integer, default=2, nullable=False
    )  # Calculated from level

    # Core stats
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)

    # Saving throws (track proficiencies)
    str_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    dex_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    con_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    int_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    wis_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    cha_save_proficient = db.Column(db.Boolean, default=False, nullable=False)

    # Combat stats
    current_hp = db.Column(db.Integer, nullable=True)
    max_hp = db.Column(db.Integer, nullable=True)
    # Temporary hit points
    temp_hp = db.Column(db.Integer, default=0, nullable=False)
    # e.g., "3d8" for level 3 fighter
    hit_dice = db.Column(db.String(20), nullable=True)
    armor_class = db.Column(db.Integer, nullable=True)
    initiative = db.Column(db.Integer, nullable=True)
    speed = db.Column(db.Integer, default=30, nullable=False)

    # Death saves
    death_save_successes = db.Column(db.Integer, default=0, nullable=False)
    death_save_failures = db.Column(db.Integer, default=0, nullable=False)

    # Resources and currencies
    gold_pieces = db.Column(db.Integer, default=0, nullable=False)
    silver_pieces = db.Column(db.Integer, default=0, nullable=False)
    copper_pieces = db.Column(db.Integer, default=0, nullable=False)
    platinum_pieces = db.Column(db.Integer, default=0, nullable=False)
    electrum_pieces = db.Column(db.Integer, default=0, nullable=False)

    # Character details and roleplay
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.String(20), nullable=True)  # e.g., "5'8\""
    weight = db.Column(db.String(20), nullable=True)  # e.g., "150 lbs"
    eyes = db.Column(db.String(30), nullable=True)
    skin = db.Column(db.String(30), nullable=True)
    hair = db.Column(db.String(30), nullable=True)
    personality_traits = db.Column(db.Text, nullable=True)
    ideals = db.Column(db.Text, nullable=True)
    bonds = db.Column(db.Text, nullable=True)
    flaws = db.Column(db.Text, nullable=True)
    backstory = db.Column(db.Text, nullable=True)

    # Extended backstory fields
    # Why is your character adventuring?
    why_adventuring = db.Column(db.Text, nullable=True)
    # What motivates your character? (comma-separated)
    motivation = db.Column(db.Text, nullable=True)
    # Where did your character grow up?
    origin = db.Column(db.Text, nullable=True)
    # Why is your character their current class?
    class_origin = db.Column(db.Text, nullable=True)
    # Special attachments to people, places, things
    attachments = db.Column(db.Text, nullable=True)
    # Does your character have a secret?
    secret = db.Column(db.Text, nullable=True)
    # What is your character like and why?
    attitude_origin = db.Column(db.Text, nullable=True)

    # Additional notes and tracking
    other_proficiencies = db.Column(db.Text, nullable=True)  # Any special proficiencies
    attacks_spellcasting = db.Column(db.Text, nullable=True)  # Attack descriptions
    # Additional features not in features table
    features_traits = db.Column(db.Text, nullable=True)

    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Enhanced character creation foreign keys
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"), nullable=True)
    subspecies_id = db.Column(
        db.Integer, db.ForeignKey("sub_species.id"), nullable=True
    )
    class_id = db.Column(db.Integer, db.ForeignKey("character_class.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Many-to-many relationships
    proficiencies = db.relationship(
        "Proficiency",
        secondary=character_proficiencies,
        lazy="subquery",
        backref=db.backref("characters", lazy=True),
    )
    languages = db.relationship(
        "Language",
        secondary=character_languages,
        lazy="subquery",
        backref=db.backref("characters", lazy=True),
    )
    features = db.relationship(
        "Feature",
        secondary=character_features,
        lazy="subquery",
        backref=db.backref("characters", lazy=True),
    )
    spells = db.relationship(
        "Spell",
        secondary=character_spells,
        lazy="subquery",
        backref=db.backref("characters", lazy=True),
    )

    # One-to-many relationship with inventory
    inventory = db.relationship(
        "CharacterItem", backref="character", lazy=True, cascade="all, delete-orphan"
    )

    # One-to-many relationship with spell slots
    spell_slots = db.relationship(
        "SpellSlot", backref="character", lazy=True, cascade="all, delete-orphan"
    )

    def get_ability_modifier(self, score):
        """Calculate ability modifier from ability score."""
        return (score - 10) // 2

    def get_saving_throw_bonus(self, ability):
        """Calculate saving throw bonus for a given ability."""
        base_modifier = self.get_ability_modifier(getattr(self, ability))
        proficiency_map = {
            "strength": self.str_save_proficient,
            "dexterity": self.dex_save_proficient,
            "constitution": self.con_save_proficient,
            "intelligence": self.int_save_proficient,
            "wisdom": self.wis_save_proficient,
            "charisma": self.cha_save_proficient,
        }

        if proficiency_map.get(ability, False):
            return base_modifier + self.proficiency_bonus
        return base_modifier

    def update_proficiency_bonus(self):
        """Update proficiency bonus based on character level."""
        if self.level >= 17:
            self.proficiency_bonus = 6
        elif self.level >= 13:
            self.proficiency_bonus = 5
        elif self.level >= 9:
            self.proficiency_bonus = 4
        elif self.level >= 5:
            self.proficiency_bonus = 3
        else:
            self.proficiency_bonus = 2

    @property
    def effective_ability_scores(self):
        """Calculate ability scores with species bonuses applied."""
        base_scores = {
            "str": self.strength,
            "dex": self.dexterity,
            "con": self.constitution,
            "int": self.intelligence,
            "wis": self.wisdom,
            "cha": self.charisma,
        }

        # Apply species bonuses
        if self.species:
            for ability, bonus in self.species.ability_score_increases.items():
                if ability in base_scores:
                    base_scores[ability] += bonus

        # Apply subspecies bonuses
        if self.subspecies and self.subspecies.additional_ability_increases:
            for ability, bonus in self.subspecies.additional_ability_increases.items():
                if ability in base_scores:
                    base_scores[ability] += bonus

        return base_scores

    @property
    def all_proficiencies(self):
        """Get all proficiencies from species, class, and individual sources."""
        proficiencies = set()

        # Add species proficiencies
        if self.species and self.species.proficiencies:
            proficiencies.update(self.species.proficiencies)

        # Add subspecies proficiencies
        if self.subspecies and self.subspecies.additional_proficiencies:
            proficiencies.update(self.subspecies.additional_proficiencies)

        # Add class proficiencies
        if self.char_class and self.char_class.skill_proficiencies:
            proficiencies.update(self.char_class.skill_proficiencies)

        # Add individual proficiencies from many-to-many relationship
        for prof in self.proficiencies:
            proficiencies.add(prof.name)

        return list(proficiencies)

    @property
    def all_languages(self):
        """Get all languages from species, subspecies, and individual sources."""
        languages = set()

        # Add species languages
        if self.species and self.species.languages:
            languages.update(self.species.languages)

        # Add subspecies languages
        if self.subspecies and self.subspecies.additional_languages:
            languages.update(self.subspecies.additional_languages)

        # Add individual languages from many-to-many relationship
        for lang in self.languages:
            languages.add(lang.name)

        return list(languages)

    @property
    def all_traits(self):
        """Get all traits from species and subspecies."""
        traits = []

        # Add species traits
        if self.species and self.species.traits:
            traits.extend(self.species.traits)

        # Add subspecies traits
        if self.subspecies and self.subspecies.additional_traits:
            traits.extend(self.subspecies.additional_traits)

        return traits

    @property
    def effective_speed(self):
        """Calculate effective speed with subspecies modifiers."""
        base_speed = self.species.speed if self.species else 30

        # Apply subspecies speed modifier
        if self.subspecies:
            base_speed += self.subspecies.speed_modifier

        return base_speed

    @property
    def effective_size(self):
        """Get effective size with subspecies override."""
        if self.subspecies and self.subspecies.size_override:
            return self.subspecies.size_override
        elif self.species:
            return self.species.size
        else:
            return "Medium"

    def __repr__(self):
        return f"<Character {self.name}>"


class Proficiency(db.Model):
    """Model for character proficiencies (skills, weapons, tools, etc.)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 'skill', 'weapon', 'tool', 'armor', etc.
    proficiency_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # For skills: 'strength', 'dexterity', etc.
    associated_ability = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Proficiency {self.name}>"


class Language(db.Model):
    """Model for character languages."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # 'Standard', 'Exotic', 'Dialect'
    language_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Language {self.name}>"


class Item(db.Model):
    """Model for equipment and inventory items."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # 'weapon', 'armor', 'tool', 'consumable', etc.
    item_type = db.Column(db.String(50), nullable=False)
    cost_gp = db.Column(db.Integer, default=0, nullable=False)
    weight_lbs = db.Column(db.Float, default=0.0, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Weapon-specific properties
    damage_dice = db.Column(db.String(20), nullable=True)  # e.g., "1d8", "2d6"
    # "slashing", "piercing", "bludgeoning", etc.
    damage_type = db.Column(db.String(30), nullable=True)
    # "melee", "ranged", "5/10" for thrown
    weapon_range = db.Column(db.String(50), nullable=True)
    # "finesse, light, versatile" etc.
    weapon_properties = db.Column(db.Text, nullable=True)
    # For versatile weapons like longsword
    versatile_damage = db.Column(db.String(20), nullable=True)

    # Armor-specific properties
    armor_class = db.Column(db.Integer, nullable=True)  # Base AC for armor
    # Max Dex bonus for medium armor
    max_dex_bonus = db.Column(db.Integer, nullable=True)
    # Minimum strength requirement
    min_strength = db.Column(db.Integer, nullable=True)
    stealth_disadvantage = db.Column(db.Boolean, default=False, nullable=False)

    # Magic item properties
    is_magical = db.Column(db.Boolean, default=False, nullable=False)
    # "common", "uncommon", "rare", "very rare", "legendary"
    rarity = db.Column(db.String(20), nullable=True)
    requires_attunement = db.Column(db.Boolean, default=False, nullable=False)
    # For items with limited uses
    charges = db.Column(db.Integer, nullable=True)

    # General properties
    # Can multiple be in one inventory slot
    stackable = db.Column(db.Boolean, default=True, nullable=False)
    consumable = db.Column(
        db.Boolean, default=False, nullable=False
    )  # Gets used up when used

    def __repr__(self):
        return f"<Item {self.name}>"


class CharacterItem(db.Model):
    """Association model for character inventory with quantity and equipment details."""

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    equipped = db.Column(db.Boolean, default=False, nullable=False)

    # Equipment slot tracking for armor and accessories
    # "main_hand", "off_hand", "armor", "helmet", etc.
    equipment_slot = db.Column(db.String(30), nullable=True)

    # Condition and customization
    # "broken", "damaged", "good", "excellent"
    condition = db.Column(db.String(20), default="good", nullable=False)
    # Custom notes about this specific item
    notes = db.Column(db.Text, nullable=True)

    # Attunement tracking for magic items
    attuned = db.Column(db.Boolean, default=False, nullable=False)

    # Charges tracking for items with limited uses
    current_charges = db.Column(db.Integer, nullable=True)

    # Relationships
    item = db.relationship("Item", backref="character_items")

    def __repr__(self):
        return f'<CharacterItem {self.quantity}x {self.item.name if self.item else "Unknown"}>'


class Feature(db.Model):
    """Model for character features from race, class, background, etc."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # 'racial', 'class', 'background', 'feat', etc.
    feature_type = db.Column(db.String(50), nullable=False)

    # Usage and limitations
    # How many times per short/long rest
    uses_per_rest = db.Column(db.Integer, nullable=True)
    # "short", "long", "none" (unlimited)
    rest_type = db.Column(db.String(20), nullable=True)
    # Minimum level to get this feature
    level_required = db.Column(db.Integer, nullable=True)

    # Class/subclass specific
    # Which class grants this feature
    source_class = db.Column(db.String(50), nullable=True)
    # Which subclass grants this feature
    source_subclass = db.Column(db.String(50), nullable=True)

    # Prerequisites and conditions
    # Any requirements to use this feature
    prerequisites = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Feature {self.name}>"


class SpellSlot(db.Model):
    """Model for tracking character spell slots."""

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # Spell slot level (1-9)
    # Total slots available
    total_slots = db.Column(db.Integer, nullable=False)
    used_slots = db.Column(
        db.Integer, default=0, nullable=False
    )  # Slots currently used

    @property
    def remaining_slots(self):
        """Calculate remaining spell slots."""
        return max(0, self.total_slots - self.used_slots)

    def use_slot(self):
        """Use one spell slot if available."""
        if self.used_slots < self.total_slots:
            self.used_slots += 1
            return True
        return False

    def restore_slot(self):
        """Restore one spell slot if any are used."""
        if self.used_slots > 0:
            self.used_slots -= 1
            return True
        return False

    def long_rest(self):
        """Restore all spell slots after a long rest."""
        self.used_slots = 0

    def __repr__(self):
        return (
            f"<SpellSlot Level {self.level}: {self.remaining_slots}/{self.total_slots}>"
        )


class Spell(db.Model):
    """Model for D&D spells."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)  # 0-9, where 0 is cantrips
    # "evocation", "illusion", etc.
    school = db.Column(db.String(30), nullable=False)

    # Casting details
    # "1 action", "1 bonus action", "10 minutes"
    casting_time = db.Column(db.String(50), nullable=True)
    # "60 feet", "Touch", "Self"
    spell_range = db.Column(db.String(50), nullable=True)
    # "V, S, M (a tiny bell)"
    components = db.Column(db.String(100), nullable=True)
    # "Instantaneous", "Concentration, up to 1 hour"
    duration = db.Column(db.String(50), nullable=True)

    # Spell description and mechanics
    description = db.Column(db.Text, nullable=False)
    # Description of casting at higher levels
    higher_level = db.Column(db.Text, nullable=True)

    # Spell lists (which classes can learn this spell)
    # Comma-separated: "wizard,sorcerer,bard"
    class_lists = db.Column(db.Text, nullable=True)

    # Source and references
    source = db.Column(db.String(50), nullable=True)  # "PHB", "XGE", etc.

    # Ritual and concentration
    is_ritual = db.Column(db.Boolean, default=False, nullable=False)
    requires_concentration = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Spell {self.name} (Level {self.level})>"


class Post(db.Model):
    """Post model for user-generated content."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to User
    author = db.relationship("User", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return f"<Post {self.title}>"


# Enhanced character creation models for Species/CharacterClass system


class Species(db.Model):
    """Species model for D&D character species (previously race)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Ability score increases as JSON: {"str": 1, "dex": 2, "con": 1}
    ability_score_increases = db.Column(db.JSON, nullable=False, default=dict)

    # Species traits and features as JSON list: ["Darkvision", "Keen Senses"]
    traits = db.Column(db.JSON, nullable=False, default=list)

    # Known languages as JSON list: ["Common", "Elvish"]
    languages = db.Column(db.JSON, nullable=False, default=list)

    # Proficiencies as JSON list: ["Perception", "Stealth"]
    proficiencies = db.Column(db.JSON, nullable=True, default=list)

    # Movement speed in feet
    speed = db.Column(db.Integer, default=30, nullable=False)

    # Size category: "Small", "Medium", "Large"
    size = db.Column(db.String(20), default="Medium", nullable=False)

    # Source book reference
    source = db.Column(db.String(50), nullable=True)

    # Optional description
    description = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationships
    subspecies = db.relationship(
        "SubSpecies", backref="species", lazy=True, cascade="all, delete-orphan"
    )
    characters = db.relationship("Character", backref="species", lazy=True)

    def __repr__(self):
        return f"<Species {self.name}>"


class CharacterClass(db.Model):
    """CharacterClass model for D&D character classes."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Hit die size (6, 8, 10, 12)
    hit_die = db.Column(db.Integer, nullable=False)

    # Primary ability score for the class
    primary_ability = db.Column(db.String(50), nullable=False)

    # Saving throw proficiencies as JSON list: ["Strength", "Constitution"]
    saving_throw_proficiencies = db.Column(db.JSON, nullable=False, default=list)

    # Available skill proficiencies as JSON list
    skill_proficiencies = db.Column(db.JSON, nullable=False, default=list)

    # Armor proficiencies as JSON list: ["Light Armor", "Medium Armor"]
    armor_proficiencies = db.Column(db.JSON, nullable=False, default=list)

    # Weapon proficiencies as JSON list: ["Simple Weapons", "Martial Weapons"]
    weapon_proficiencies = db.Column(db.JSON, nullable=False, default=list)

    # Number of skill proficiencies to choose
    skill_choices = db.Column(db.Integer, default=2, nullable=False)

    # Spellcasting ability (if applicable)
    spellcasting_ability = db.Column(db.String(20), nullable=True)

    # Class features and progression (could be expanded later)
    class_features = db.Column(db.JSON, nullable=True, default=dict)

    # Source book reference
    source = db.Column(db.String(50), nullable=True)

    # Optional description
    description = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationships
    characters = db.relationship("Character", backref="char_class", lazy=True)

    def __repr__(self):
        return f"<CharacterClass {self.name}>"


class SubSpecies(db.Model):
    """SubSpecies model for species variants (e.g., High Elf, Wood Elf)."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Foreign key to parent species
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"), nullable=False)

    # Additional traits specific to this subspecies
    additional_traits = db.Column(db.JSON, nullable=True, default=list)

    # Additional ability score increases (beyond species base)
    additional_ability_increases = db.Column(db.JSON, nullable=True, default=dict)

    # Additional proficiencies
    additional_proficiencies = db.Column(db.JSON, nullable=True, default=list)

    # Additional languages
    additional_languages = db.Column(db.JSON, nullable=True, default=list)

    # Speed modifier (if different from base species)
    speed_modifier = db.Column(db.Integer, default=0, nullable=False)

    # Size override (if different from base species)
    size_override = db.Column(db.String(20), nullable=True)

    # Source book reference
    source = db.Column(db.String(50), nullable=True)

    # Optional description
    description = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationships
    characters = db.relationship("Character", backref="subspecies", lazy=True)

    def __repr__(self):
        return f"<SubSpecies {self.name}>"
