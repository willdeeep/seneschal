"""
CharacterClass model for D&D character classes.

This module contains the CharacterClass model that defines character class
information including hit dice, abilities, proficiencies, and class-specific
features for D&D characters.
"""

from project import db


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
