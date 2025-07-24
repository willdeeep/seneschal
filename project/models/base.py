"""
Base models and shared database configuration.

This module contains shared database imports, association tables, and base classes
used across all model files in the modular structure.
"""

from project import db


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
