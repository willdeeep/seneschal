"""
Species and SubSpecies models for D&D character species.

This module contains the Species and SubSpecies models that define character
species (previously race) information including ability score increases,
traits, languages, proficiencies, and other species-specific characteristics.
"""

from project import db


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
