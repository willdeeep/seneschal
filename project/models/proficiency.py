"""
Proficiency and Language models.

This module contains models for character proficiencies (skills, weapons, tools, etc.)
and languages that characters can know.
"""

from project import db


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
