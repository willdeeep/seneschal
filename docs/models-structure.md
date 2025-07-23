# Models Module Structure

This document describes the modular structure of the models package, implemented as part of Issue #5.

## Overview

The models package has been refactored from a single monolithic `models.py` file into a modular structure where each model class has its own dedicated file. This improves maintainability, readability, and development workflow.

## File Structure

```
project/models/
├── __init__.py              # Import all models, maintain API compatibility
├── base.py                  # Shared base classes and association tables
├── user.py                  # User model for authentication
├── character.py             # Character model (main D&D character)
├── species.py               # Species and SubSpecies models
├── character_class.py       # CharacterClass model
├── proficiency.py           # Proficiency and Language models
├── item.py                  # Item and CharacterItem models
├── feature.py               # Feature model
├── spell.py                 # Spell and SpellSlot models
└── post.py                  # Post model for user content
```

## Module Descriptions

### base.py
- Contains shared database association tables
- Defines many-to-many relationship tables:
  - `character_proficiencies`
  - `character_languages`
  - `character_features`
  - `character_spells`

### user.py
- `User` model for authentication and user management
- Includes password hashing and validation methods
- Relationships to characters and posts

### character.py
- `Character` model - the main D&D character sheet
- Complete character stats, abilities, inventory, spells
- Computed properties for ability scores, proficiencies, languages
- Methods for level progression and saving throws

### species.py
- `Species` model for D&D character species (races)
- `SubSpecies` model for species variants (e.g., High Elf, Wood Elf)
- Ability score increases, traits, languages, proficiencies

### character_class.py
- `CharacterClass` model for D&D character classes
- Hit dice, abilities, proficiencies, class features
- Spellcasting information for magical classes

### proficiency.py
- `Proficiency` model for skills, weapons, tools, armor
- `Language` model for character languages
- Type categorization and ability associations

### item.py
- `Item` model for equipment and inventory items
- `CharacterItem` association model for character inventory
- Weapon properties, armor stats, magic item characteristics

### feature.py
- `Feature` model for character features and traits
- Racial, class, background, and feat features
- Usage limitations and prerequisites

### spell.py
- `Spell` model for D&D spells
- `SpellSlot` model for tracking character spell slots
- Spell mechanics, components, and slot management

### post.py
- `Post` model for user-generated content
- Community features and content management

## Backward Compatibility

The original `project/models.py` file now imports all models from the modular structure, maintaining complete backward compatibility. All existing imports continue to work:

```python
# These imports work exactly as before
from project.models import User, Character, Species, CharacterClass
from project.models import Spell, Item, db
```

## Benefits

1. **Easier Navigation** - Find specific model logic quickly
2. **Reduced Merge Conflicts** - Team members can work on different models simultaneously
3. **Better Testing** - Unit tests can focus on individual model files
4. **Cleaner Git History** - Changes to specific models are isolated
5. **Future Scalability** - Easy to add new model types

## Migration Notes

- **Zero Breaking Changes** - All existing imports work unchanged
- **All Tests Pass** - No modifications required to existing test suite
- **Database Unchanged** - All relationships and constraints preserved
- **Full Functionality** - All computed properties and methods preserved

## Development Guidelines

### For New Code
Consider importing directly from specific modules:
```python
from project.models.user import User
from project.models.species import Species
from project.models.character_class import CharacterClass
```

### For Existing Code
Continue using existing import patterns - no changes required:
```python
from project.models import User, Character, Species, CharacterClass
```

## Testing

All existing tests pass without modification, confirming that:
- Model functionality is preserved
- Database relationships work correctly
- Import compatibility is maintained
- No circular dependencies exist

Run tests with:
```bash
python -m pytest tests/ -v
```

## Future Additions

When adding new models:
1. Create a new file in `project/models/`
2. Add the model import to `__init__.py`
3. Add the model name to `__all__` list
4. Follow the established pattern for documentation and structure
