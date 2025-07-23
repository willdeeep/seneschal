"""
Character model for D&D character sheets.

This module contains the Character model that represents a complete D&D character
with all their stats, abilities, inventory, spells, and relationships to other
models like Species, CharacterClass, and User.
"""

from project import db
from .base import character_proficiencies, character_languages, character_features, character_spells


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
