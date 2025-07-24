"""
Feature model for character features and traits.

This module contains the Feature model that represents character features
from race, class, background, feats, and other sources.
"""

from project import db


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
