# Seneschal Project: Model Inheritance and Relationship Documentation

## Project Overview
This document illustrates the inheritance patterns, database relationships, and key properties/methods across all models in the Seneschal D&D character management system.

## ASCII Inheritance Hierarchy

```
Flask-SQLAlchemy db.Model (Base Class)
│
├── User
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── username
│   │   ├── email
│   │   ├── password_hash
│   │   ├── created_at
│   │   └── last_login
│   │
│   ├── Relationships:
│   │   └── characters (One-to-Many → Character)
│   │
│   └── Methods:
│       ├── check_password()
│       ├── set_password()
│       └── __repr__()
│
├── Character (Central Hub Model)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, player_name, level
│   │   ├── background (text field)
│   │   ├── ability scores (str, dex, con, int, wis, cha)
│   │   ├── combat stats (hp, ac, initiative, speed)
│   │   ├── backstory fields (personality_traits, ideals, bonds, flaws)
│   │   ├── extended backstory (why_adventuring, motivation, etc.)
│   │   └── timestamps (created_at, updated_at)
│   │
│   ├── Foreign Keys:
│   │   ├── user_id → User.id
│   │   ├── species_id → Species.id
│   │   ├── subspecies_id → SubSpecies.id
│   │   ├── class_id → CharacterClass.id
│   │   └── background_id → Background.id
│   │
│   ├── Direct Relationships:
│   │   ├── species (Many-to-One → Species)
│   │   ├── subspecies (Many-to-One → SubSpecies)
│   │   ├── char_class (Many-to-One → CharacterClass)
│   │   └── char_background (Many-to-One → Background)
│   │
│   ├── Many-to-Many Relationships:
│   │   ├── proficiencies (via character_proficiencies table)
│   │   ├── languages (via character_languages table)
│   │   ├── features (via character_features table)
│   │   └── spells (via character_spells table)
│   │
│   ├── One-to-Many Relationships:
│   │   ├── inventory → CharacterItem
│   │   ├── spell_slots → SpellSlot
│   │   └── equipment_items → CharacterEquipment
│   │
│   └── Methods:
│       ├── get_ability_modifier(score)
│       ├── get_saving_throw_bonus(ability)
│       ├── calculate_proficiency_bonus()
│       ├── get_effective_ability_scores() [computed with species bonuses]
│       ├── get_all_proficiencies() [combined from all sources]
│       ├── get_all_languages() [combined from all sources]
│       ├── get_all_traits() [combined from species/class/background]
│       └── __repr__()
│
├── Species (Core D&D Race System)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name (unique)
│   │   ├── ability_score_increases (JSON: {"str": 2, "dex": 1})
│   │   ├── traits (JSON: ["Darkvision", "Keen Senses"])
│   │   ├── languages (JSON: ["Common", "Elvish"])
│   │   ├── proficiencies (JSON: ["Perception"])
│   │   ├── speed (integer, default 30)
│   │   └── size (string, default "Medium")
│   │
│   ├── Relationships:
│   │   ├── subspecies (One-to-Many → SubSpecies) [backref: "species"]
│   │   └── characters (One-to-Many → Character) [backref: "species"]
│   │
│   └── Methods:
│       ├── get_ability_bonus(ability_name)
│       ├── get_total_traits() [includes inherited traits]
│       └── __repr__()
│
├── SubSpecies (Species Variants)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name
│   │   ├── species_id (Foreign Key → Species.id)
│   │   └── additional_traits (JSON: extra traits beyond base species)
│   │
│   ├── Relationships:
│   │   ├── species (Many-to-One → Species) [via backref]
│   │   └── characters (One-to-Many → Character) [backref: "subspecies"]
│   │
│   └── Methods:
│       ├── get_combined_traits() [species + subspecies traits]
│       └── __repr__()
│
├── CharacterClass (D&D Class System)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name (unique)
│   │   ├── hit_die (integer: 6, 8, 10, 12)
│   │   ├── primary_ability (string: "Strength", "Dexterity", etc.)
│   │   ├── saving_throw_proficiencies (JSON: ["Strength", "Constitution"])
│   │   ├── skill_proficiencies (JSON: list of available skills)
│   │   ├── armor_proficiencies (JSON: ["Light Armor", "Shields"])
│   │   └── weapon_proficiencies (JSON: ["Simple Weapons", "Martial"])
│   │
│   ├── Relationships:
│   │   └── characters (One-to-Many → Character) [backref: "char_class"]
│   │
│   └── Methods:
│       ├── get_max_skill_proficiencies() [class-specific limits]
│       ├── is_spellcaster()
│       ├── get_spellcasting_ability()
│       └── __repr__()
│
├── Background (NEW - D&D Background System)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name (unique)
│   │   ├── description (text)
│   │   ├── skill_proficiencies (JSON: ["Insight", "Religion"])
│   │   ├── tool_proficiencies (JSON: ["Thieves' Tools"])
│   │   ├── languages (JSON: ["Any two languages"])
│   │   ├── equipment (JSON: starting equipment list)
│   │   ├── feature_name (string)
│   │   ├── feature_description (text)
│   │   ├── personality_traits (JSON: trait options)
│   │   ├── ideals (JSON: ideal options)
│   │   ├── bonds (JSON: bond options)
│   │   ├── flaws (JSON: flaw options)
│   │   └── starting_gold (integer)
│   │
│   ├── Relationships:
│   │   └── characters (One-to-Many → Character) [via char_background]
│   │
│   └── Methods:
│       ├── get_popular_backgrounds() [class method]
│       └── __repr__()
│
├── Equipment (NEW - D&D Items System)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, category, description
│   │   ├── cost_cp (cost in copper pieces)
│   │   ├── weight (float)
│   │   ├── weapon properties (damage_dice, damage_type, weapon_properties)
│   │   ├── armor properties (armor_class, max_dex_bonus, min_strength, stealth_disadvantage)
│   │   └── magic properties (rarity, requires_attunement, magic_bonus)
│   │
│   ├── Relationships:
│   │   └── character_items (One-to-Many → CharacterEquipment)
│   │
│   └── Methods:
│       ├── get_starting_equipment_for_class(class_name) [class method]
│       └── __repr__()
│
├── Spell (Existing - D&D Spells System)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name (unique), level (0-9), school
│   │   ├── casting properties (casting_time, spell_range, components, duration)
│   │   ├── description, higher_level
│   │   ├── class_lists (text: comma-separated class names)
│   │   ├── source, is_ritual, requires_concentration
│   │   └── available_to_classes (JSON: list of class names)
│   │
│   ├── Relationships:
│   │   ├── characters (Many-to-Many via character_spells table)
│   │   └── character_instances (One-to-Many → CharacterSpell)
│   │
│   └── Methods:
│       ├── get_cantrips_for_class(class_name) [class method]
│       ├── get_spells_for_class_and_level(class_name, level) [class method]
│       └── __repr__()
│
├── Proficiency (Existing)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, category, description
│   │   └── source
│   │
│   ├── Relationships:
│   │   └── characters (Many-to-Many via character_proficiencies table)
│   │
│   └── Methods:
│       └── __repr__()
│
├── Language (Existing)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, script, speakers
│   │   └── rarity
│   │
│   ├── Relationships:
│   │   └── characters (Many-to-Many via character_languages table)
│   │
│   └── Methods:
│       └── __repr__()
│
├── Feature (Existing)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, description, source
│   │   └── prerequisite
│   │
│   ├── Relationships:
│   │   └── characters (Many-to-Many via character_features table)
│   │
│   └── Methods:
│       └── __repr__()
│
├── Item (Existing - Legacy Equipment)
│   │
│   ├── Properties:
│   │   ├── id (Primary Key)
│   │   ├── name, category, description
│   │   ├── cost, weight, rarity
│   │   └── properties
│   │
│   ├── Relationships:
│   │   └── character_items (One-to-Many → CharacterItem)
│   │
│   └── Methods:
│       └── __repr__()
│
└── Junction/Association Models:
    │
    ├── CharacterItem (Character ↔ Item)
    │   ├── character_id, item_id, quantity, equipped
    │   └── character, item relationships
    │
    ├── CharacterEquipment (NEW: Character ↔ Equipment)
    │   ├── character_id, equipment_id, quantity, equipped, attuned
    │   └── character, equipment relationships
    │
    ├── CharacterSpell (NEW: Character ↔ Spell)
    │   ├── character_id, spell_id, known, prepared
    │   ├── learned_at_level, source
    │   └── character, spell relationships
    │
    └── SpellSlot (Character Spell Slots)
        ├── character_id, level, total_slots, used_slots
        └── character relationship
```

## Database Relationship Mapping

```
Association Tables (Many-to-Many):
┌─────────────────────────┐    ┌────────────────────────┐    ┌─────────────────────────┐
│ character_proficiencies │    │   character_languages  │    │   character_features    │
├─────────────────────────┤    ├────────────────────────┤    ├─────────────────────────┤
│ character_id (FK)       │    │ character_id (FK)      │    │ character_id (FK)       │
│ proficiency_id (FK)     │    │ language_id (FK)       │    │ feature_id (FK)         │
└─────────────────────────┘    └────────────────────────┘    └─────────────────────────┘

┌─────────────────────────┐
│   character_spells      │
├─────────────────────────┤
│ character_id (FK)       │
│ spell_id (FK)           │
└─────────────────────────┘

Foreign Key Relationships (Many-to-One):
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User      │    │  Species    │    │ CharacterClass  │    │  Background     │
├─────────────┤    ├─────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)     │←───│ id (PK)     │    │ id (PK)         │    │ id (PK)         │
│ username    │    │ name        │    │ name            │    │ name            │
│ email       │    │ traits      │    │ hit_die         │    │ description     │
│ ...         │    │ ...         │    │ ...             │    │ ...             │
└─────────────┘    └─────────────┘    └─────────────────┘    └─────────────────┘
      │                   │                     │                     │
      │                   │                     │                     │
      └───────────────────┼─────────────────────┼─────────────────────┼──────────┐
                          │                     │                     │          │
                          │                     │                     │          │
                          ▼                     ▼                     ▼          │
┌─────────────────────────────────────────────────────────────────────────────┐  │
│                           Character                                         │  │
├─────────────────────────────────────────────────────────────────────────────┤  │
│ id (PK)                 |                     |                     |       │  │
│ user_id (FK) ───────────┼─────────────────────┼─────────────────────┼───────┼──┘
│ species_id (FK) ────────┘                     |                     |       |
│ subspecies_id (FK) ─────────────────────────┐ |                     |       |
│ class_id (FK) ──────────────────────────────┼─┘                     |       |
│ background_id (FK) ─────────────────────────┼───────────────────────┘       |
│ name, level, ability_scores...              │                               |
│ personality_traits, ideals, bonds, flaws    │                               |
│ combat_stats, backstory...                  │                               |
└─────────────────────────────────────────────┼───────────────────────────────┘
                                              │
                        ┌─────────────────────┘
                        │
                        ▼
              ┌───────────────────┐
              │   SubSpecies      │
              ├───────────────────┤
              │ id (PK)           │
              │ species_id (FK)   │
              │ name              │
              │ additional_traits │
              └───────────────────┘
                        │
                        │ species_id
                        │
                        ▼
              ┌─────────────────┐
              │    Species      │
              ├─────────────────┤
              │ id (PK)         │
              │ name            │
              │ ability_bonuses │
              │ traits          │
              │ ...             │
              └─────────────────┘
```

## Key Inheritance Patterns

### 1. **SQLAlchemy Model Inheritance**
All models inherit from `db.Model` which provides:
- Primary key management
- Query interface (`Model.query`)
- Session management
- Metadata and table creation

### 2. **Character as Central Hub**
The Character model serves as the central aggregation point:
- **Direct relationships**: User, Species, SubSpecies, CharacterClass, Background
- **Many-to-many**: Proficiencies, Languages, Features, Spells
- **One-to-many**: Equipment, Items, SpellSlots

### 3. **Computed Properties Pattern**
Several models implement computed properties that combine data:
- `Character.get_effective_ability_scores()`: base + species bonuses
- `Character.get_all_proficiencies()`: class + species + background
- `Species.get_total_traits()`: includes subspecies traits

### 4. **Backref Relationships**
Bidirectional relationships established via backrefs:
- `Species.characters` ↔ `Character.species`
- `CharacterClass.characters` ↔ `Character.char_class`
- `User.characters` ↔ `Character.user`

## Critical Dependencies to Preserve

### 1. **Existing Backref Names**
- `Character.species` (from Species model)
- `Character.char_class` (from CharacterClass model)
- `Character.subspecies` (from SubSpecies model)

### 2. **Foreign Key Constraints**
- All character relationships use nullable FKs for flexibility
- Junction tables enforce referential integrity

### 3. **JSON Field Structures**
- Species: `ability_score_increases`, `traits`, `languages`, `proficiencies`
- CharacterClass: `skill_proficiencies`, `armor_proficiencies`, etc.
- Background: `skill_proficiencies`, `equipment`, `personality_traits`, etc.

### 4. **API Integration Points**
- Character creation endpoints expect specific FK field names
- Proficiency API uses class-specific limits
- Species/subspecies filtering logic depends on relationships

## New Advanced Customization Features

### Added Models:
1. **Background**: D&D 5e backgrounds with proficiencies, equipment, features
2. **Equipment**: Enhanced item system with weapon/armor properties
3. **CharacterEquipment**: Junction for character equipment with quantity/equipped status
4. **CharacterSpell**: Junction for character spells with known/prepared status

### Enhanced APIs:
1. `/api/backgrounds` - Background selection
2. `/api/equipment` - Class/background-based equipment
3. `/api/cantrips` - Class-specific cantrips
4. `/api/starting-spells` - 1st level spells for classes
5. `/api/character-optimization` - Build suggestions

### Frontend Enhancements:
1. Ability score generation methods (Standard Array, Point Buy, Rolling, Custom)
2. Dynamic background selection with feature display
3. Equipment selection based on class/background
4. Spell selection for spellcasting classes
5. Character optimization suggestions

## Testing Considerations

When modifying this system:
1. **Preserve existing relationships** - Character model relationships are tested extensively
2. **Maintain backref consistency** - Changing backref names breaks existing code
3. **JSON field compatibility** - API endpoints expect specific JSON structures
4. **Foreign key cascading** - Some relationships use cascade delete
5. **Computed property dependencies** - Methods rely on specific relationship names

This inheritance structure provides a solid foundation for D&D 5e character management while maintaining flexibility for future enhancements.
