"""
Models module for backward compatibility.

This module maintains backward compatibility by importing all models from the 
new modular structure. All existing imports should continue to work unchanged.

For new code, consider importing directly from the specific model modules:
    from project.models.user import User
    from project.models.species import Species
    from project.models.character_class import CharacterClass
"""

# Import all models from the modular structure to maintain compatibility
from .models import *  # noqa: F401,F403

# Backward compatibility - these imports should work exactly as before
# from project.models import User, Character, Species, CharacterClass, etc.
