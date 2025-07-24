"""
Models module initialization.

This module imports all model classes from their individual files and exposes them
to maintain backward compatibility with existing imports. All models remain accessible
through the same import patterns as before the refactoring.

Example usage:
    from project.models import Species, CharacterClass, Character, User
    from project.models import Spell, SpellSlot, Item, Feature
"""

# Import shared database components
from project import db
from .base import character_proficiencies, character_languages, character_features, character_spells

# Import all model classes
from .user import User
from .species import Species, SubSpecies
from .character_class import CharacterClass
from .character import Character
from .proficiency import Proficiency, Language
from .item import Item, CharacterItem
from .feature import Feature
from .spell import Spell, SpellSlot
from .post import Post

# Define what gets imported with "from project.models import *"
__all__ = [
    # Database components
    'db',
    'character_proficiencies',
    'character_languages',
    'character_features',
    'character_spells',

    # Core models
    'User',
    'Character',
    'Species',
    'SubSpecies',
    'CharacterClass',

    # Supporting models
    'Proficiency',
    'Language',
    'Item',
    'CharacterItem',
    'Feature',
    'Spell',
    'SpellSlot',
    'Post',
]
