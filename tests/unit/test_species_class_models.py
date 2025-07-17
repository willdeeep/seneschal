"""
Test cases for the Species and CharacterClass models.
This module tests the first stage of the species-class feature implementation.
These tests are marked as skip since they test features in development.
"""

import pytest
from project.models import Character, db
from project import create_app


@pytest.mark.unit
class TestSpeciesModel:
    """Unit tests for the Species model."""

    def test_species_creation_basic(self, app):
        """
        GIVEN: A new Species with basic attributes
        WHEN: The Species is created
        THEN: The Species should be created with correct attributes
        """
        with app.app_context():
            # Import here to avoid circular imports in development
            from project.models import Species
            
            species = Species(
                name='Human',
                ability_score_increases={'str': 1, 'dex': 1, 'con': 1, 'int': 1, 'wis': 1, 'cha': 1},
                traits=['Extra Language', 'Extra Skill'],
                languages=['Common'],
                speed=30,
                size='Medium'
            )
            
            assert species.name == 'Human'
            assert species.ability_score_increases == {'str': 1, 'dex': 1, 'con': 1, 'int': 1, 'wis': 1, 'cha': 1}
            assert species.traits == ['Extra Language', 'Extra Skill']
            assert species.languages == ['Common']
            assert species.speed == 30
            assert species.size == 'Medium'

    def test_species_creation_elf(self, app):
        """
        GIVEN: A new Elf Species with specific attributes
        WHEN: The Species is created
        THEN: The Species should be created with Elf-specific attributes
        """
        with app.app_context():
            from project.models import Species
            
            species = Species(
                name='Elf',
                ability_score_increases={'dex': 2},
                traits=['Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance'],
                languages=['Common', 'Elvish'],
                proficiencies=['Perception'],
                speed=30,
                size='Medium'
            )
            
            assert species.name == 'Elf'
            assert species.ability_score_increases == {'dex': 2}
            assert 'Darkvision' in species.traits
            assert 'Elvish' in species.languages
            assert 'Perception' in species.proficiencies

    def test_species_representation(self, app):
        """
        GIVEN: A Species instance
        WHEN: The Species is converted to string representation
        THEN: It should return the name in the format '<Species name>'
        """
        with app.app_context():
            from project.models import Species
            
            species = Species(name='Dwarf')
            assert str(species) == '<Species Dwarf>'


@pytest.mark.unit
class TestCharacterClassModel:
    """Unit tests for the CharacterClass model."""

    def test_character_class_creation_wizard(self, app):
        """
        GIVEN: A new Wizard CharacterClass
        WHEN: The CharacterClass is created
        THEN: The CharacterClass should be created with wizard-specific attributes
        """
        with app.app_context():
            from project.models import CharacterClass
            
            char_class = CharacterClass(
                name='Wizard',
                hit_die=6,
                primary_ability='Intelligence',
                saving_throw_proficiencies=['Intelligence', 'Wisdom'],
                skill_proficiencies=['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion'],
                armor_proficiencies=[],
                weapon_proficiencies=['Daggers', 'Darts', 'Slings', 'Quarterstaffs', 'Light Crossbows']
            )
            
            assert char_class.name == 'Wizard'
            assert char_class.hit_die == 6
            assert char_class.primary_ability == 'Intelligence'
            assert 'Intelligence' in char_class.saving_throw_proficiencies
            assert 'Arcana' in char_class.skill_proficiencies
            assert 'Daggers' in char_class.weapon_proficiencies
            assert len(char_class.armor_proficiencies) == 0

    def test_character_class_creation_fighter(self, app):
        """
        GIVEN: A new Fighter CharacterClass
        WHEN: The CharacterClass is created
        THEN: The CharacterClass should be created with fighter-specific attributes
        """
        with app.app_context():
            from project.models import CharacterClass
            
            char_class = CharacterClass(
                name='Fighter',
                hit_die=10,
                primary_ability='Strength',
                saving_throw_proficiencies=['Strength', 'Constitution'],
                skill_proficiencies=['Acrobatics', 'Animal Handling', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival'],
                armor_proficiencies=['Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields'],
                weapon_proficiencies=['Simple Weapons', 'Martial Weapons']
            )
            
            assert char_class.name == 'Fighter'
            assert char_class.hit_die == 10
            assert char_class.primary_ability == 'Strength'
            assert 'Constitution' in char_class.saving_throw_proficiencies
            assert 'Athletics' in char_class.skill_proficiencies
            assert 'Heavy Armor' in char_class.armor_proficiencies
            assert 'Martial Weapons' in char_class.weapon_proficiencies

    def test_character_class_representation(self, app):
        """
        GIVEN: A CharacterClass instance
        WHEN: The CharacterClass is converted to string representation
        THEN: It should return the name in the format '<CharacterClass name>'
        """
        with app.app_context():
            from project.models import CharacterClass
            
            char_class = CharacterClass(name='Rogue')
            assert str(char_class) == '<CharacterClass Rogue>'


@pytest.mark.skip(reason="Testing features in development - Species/CharacterClass models")
@pytest.mark.unit
class TestSubSpeciesModel:
    """Unit tests for the SubSpecies model."""

    def test_subspecies_creation_high_elf(self, app):
        """
        GIVEN: A new High Elf SubSpecies
        WHEN: The SubSpecies is created
        THEN: The SubSpecies should be created with high elf-specific attributes
        """
        with app.app_context():
            from project.models import Species, SubSpecies
            
            # Create parent species first
            elf_species = Species(name='Elf')
            db.session.add(elf_species)
            db.session.flush()  # Get the ID without committing
            
            subspecies = SubSpecies(
                name='High Elf',
                species_id=elf_species.id,
                additional_traits=['Cantrip', 'Longsword Proficiency']
            )
            
            assert subspecies.name == 'High Elf'
            assert subspecies.species_id == elf_species.id
            assert 'Cantrip' in subspecies.additional_traits
            assert 'Longsword Proficiency' in subspecies.additional_traits

    def test_subspecies_creation_wood_elf(self, app):
        """
        GIVEN: A new Wood Elf SubSpecies
        WHEN: The SubSpecies is created
        THEN: The SubSpecies should be created with wood elf-specific attributes
        """
        with app.app_context():
            from project.models import Species, SubSpecies
            
            # Create parent species first
            elf_species = Species(name='Elf')
            db.session.add(elf_species)
            db.session.flush()  # Get the ID without committing
            
            subspecies = SubSpecies(
                name='Wood Elf',
                species_id=elf_species.id,
                additional_traits=['Mask of the Wild', 'Longsword Proficiency', 'Longbow Proficiency']
            )
            
            assert subspecies.name == 'Wood Elf'
            assert subspecies.species_id == elf_species.id
            assert 'Mask of the Wild' in subspecies.additional_traits
            assert 'Longbow Proficiency' in subspecies.additional_traits

    def test_subspecies_representation(self, app):
        """
        GIVEN: A SubSpecies instance
        WHEN: The SubSpecies is converted to string representation
        THEN: It should return the name in the format '<SubSpecies name>'
        """
        with app.app_context():
            from project.models import SubSpecies
            
            subspecies = SubSpecies(name='Drow')
            assert str(subspecies) == '<SubSpecies Drow>'


@pytest.mark.functional
class TestCharacterSpeciesClassIntegration:
    """Integration tests for Character with Species and CharacterClass relationships."""

    def test_character_with_species_relationship(self, persistent_test_user, app):
        """
        GIVEN: A Character with a Species
        WHEN: The Character is created with species relationship
        THEN: The Character should have proper species relationship
        """
        with app.app_context():
            from project.models import Species, Character
            
            # Create species
            species = Species(
                name='Human',
                ability_score_increases={'str': 1, 'dex': 1, 'con': 1, 'int': 1, 'wis': 1, 'cha': 1},
                traits=['Extra Language', 'Extra Skill'],
                languages=['Common'],
                speed=30,
                size='Medium'
            )
            db.session.add(species)
            db.session.flush()
            
            # Create character with species
            character = Character(
                name='Test Human',
                species_id=species.id,                level=1,
                strength=15,
                dexterity=14,
                constitution=13,
                intelligence=12,
                wisdom=10,
                charisma=8,
                user_id=persistent_test_user.id
            )
            db.session.add(character)
            db.session.flush()
            
            # Test relationship
            assert character.species is not None
            assert character.species.name == 'Human'
            assert character.species.speed == 30
            assert 'Common' in character.species.languages

    def test_character_with_class_relationship(self, persistent_test_user, app):
        """
        GIVEN: A Character with a CharacterClass
        WHEN: The Character is created with class relationship
        THEN: The Character should have proper class relationship
        """
        with app.app_context():
            from project.models import CharacterClass, Character
            
            # Create character class
            char_class = CharacterClass(
                name='Wizard',
                hit_die=6,
                primary_ability='Intelligence',
                saving_throw_proficiencies=['Intelligence', 'Wisdom'],
                skill_proficiencies=['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion'],
                armor_proficiencies=[],
                weapon_proficiencies=['Daggers', 'Darts', 'Slings', 'Quarterstaffs', 'Light Crossbows']
            )
            db.session.add(char_class)
            db.session.flush()
            
            # Create character with class
            character = Character(
                name='Test Wizard',                class_id=char_class.id,
                level=1,
                strength=8,
                dexterity=14,
                constitution=12,
                intelligence=15,
                wisdom=13,
                charisma=10,
                user_id=persistent_test_user.id
            )
            db.session.add(character)
            db.session.flush()
            
            # Test relationship
            assert character.char_class is not None
            assert character.char_class.name == 'Wizard'
            assert character.char_class.hit_die == 6
            assert character.char_class.primary_ability == 'Intelligence'
            assert 'Arcana' in character.char_class.skill_proficiencies

    def test_character_with_species_and_class(self, character_lifecycle_setup, app):
        """
        GIVEN: A Character with both Species and CharacterClass
        WHEN: The Character is created using lifecycle setup
        THEN: The Character should have proper relationships and computed properties
        """
        with app.app_context():
            from project.models import Species, CharacterClass, Character
            
            lifecycle = character_lifecycle_setup
            
            # Create species
            species = Species(
                name='Elf',
                ability_score_increases={'dex': 2},
                traits=['Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance'],
                languages=['Common', 'Elvish'],
                proficiencies=['Perception'],
                speed=30,
                size='Medium'
            )
            db.session.add(species)
            db.session.flush()
            
            # Create character class
            char_class = CharacterClass(
                name='Wizard',
                hit_die=6,
                primary_ability='Intelligence',
                saving_throw_proficiencies=['Intelligence', 'Wisdom'],
                skill_proficiencies=['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion'],
                armor_proficiencies=[],
                weapon_proficiencies=['Daggers', 'Darts', 'Slings', 'Quarterstaffs', 'Light Crossbows']
            )
            db.session.add(char_class)
            db.session.flush()
            
            # Create character with both species and class
            character = lifecycle.create_character(
                name='Elven Wizard',                species_id=species.id,
                class_id=char_class.id,
                level=1,
                strength=8,
                dexterity=14,
                constitution=12,
                intelligence=15,
                wisdom=13,
                charisma=10
            )
            
            # Test relationships
            assert character.species is not None
            assert character.species.name == 'Elf'
            assert character.char_class is not None
            assert character.char_class.name == 'Wizard'
            
            # Test computed properties (when implemented)
            # These would be implemented as part of the Species/CharacterClass feature
            # assert character.effective_ability_scores['dex'] == 16  # 14 + 2 from Elf
            # assert 'Perception' in character.all_proficiencies
            # assert 'Arcana' in character.all_proficiencies

    def test_character_with_subspecies(self, persistent_test_user, app):
        """
        GIVEN: A Character with a SubSpecies
        WHEN: The Character is created with subspecies relationship
        THEN: The Character should have proper subspecies relationship
        """
        with app.app_context():
            from project.models import Species, SubSpecies, Character
            
            # Create species
            species = Species(name='Elf')
            db.session.add(species)
            db.session.flush()
            
            # Create subspecies
            subspecies = SubSpecies(
                name='High Elf',
                species_id=species.id,
                additional_traits=['Cantrip', 'Longsword Proficiency']
            )
            db.session.add(subspecies)
            db.session.flush()
            
            # Create character with subspecies
            character = Character(
                name='High Elf Wizard',
                species_id=species.id,
                subspecies_id=subspecies.id,                level=1,
                strength=8,
                dexterity=14,
                constitution=12,
                intelligence=15,
                wisdom=13,
                charisma=10,
                user_id=persistent_test_user.id
            )
            db.session.add(character)
            db.session.flush()
            
            # Test relationships
            assert character.species is not None
            assert character.species.name == 'Elf'
            assert character.subspecies is not None
            assert character.subspecies.name == 'High Elf'
            assert 'Cantrip' in character.subspecies.additional_traits


@pytest.mark.skip(reason="Testing features in development - Species/CharacterClass models")
@pytest.mark.functional
class TestSpeciesClassPersistence:
    """Test persistence of Species and CharacterClass models."""

    def test_species_persistence(self, app):
        """
        GIVEN: A Species that is saved to the database
        WHEN: The Species is retrieved from the database
        THEN: The Species should have all its attributes preserved
        """
        with app.app_context():
            from project.models import Species
            
            # Create and save species
            species = Species(
                name='Dragonborn',
                ability_score_increases={'str': 2, 'cha': 1},
                traits=['Draconic Ancestry', 'Breath Weapon', 'Damage Resistance'],
                languages=['Common', 'Draconic'],
                speed=30,
                size='Medium'
            )
            db.session.add(species)
            db.session.commit()
            
            # Retrieve species
            retrieved_species = Species.query.filter_by(name='Dragonborn').first()
            
            assert retrieved_species is not None
            assert retrieved_species.name == 'Dragonborn'
            assert retrieved_species.ability_score_increases == {'str': 2, 'cha': 1}
            assert 'Breath Weapon' in retrieved_species.traits
            assert 'Draconic' in retrieved_species.languages

    def test_character_class_persistence(self, app):
        """
        GIVEN: A CharacterClass that is saved to the database
        WHEN: The CharacterClass is retrieved from the database
        THEN: The CharacterClass should have all its attributes preserved
        """
        with app.app_context():
            from project.models import CharacterClass
            
            # Create and save character class
            char_class = CharacterClass(
                name='Rogue',
                hit_die=8,
                primary_ability='Dexterity',
                saving_throw_proficiencies=['Dexterity', 'Intelligence'],
                skill_proficiencies=['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth'],
                armor_proficiencies=['Light Armor'],
                weapon_proficiencies=['Simple Weapons', 'Hand Crossbows', 'Longswords', 'Rapiers', 'Shortswords']
            )
            db.session.add(char_class)
            db.session.commit()
            
            # Retrieve character class
            retrieved_class = CharacterClass.query.filter_by(name='Rogue').first()
            
            assert retrieved_class is not None
            assert retrieved_class.name == 'Rogue'
            assert retrieved_class.hit_die == 8
            assert retrieved_class.primary_ability == 'Dexterity'
            assert 'Dexterity' in retrieved_class.saving_throw_proficiencies
            assert 'Stealth' in retrieved_class.skill_proficiencies
            assert 'Light Armor' in retrieved_class.armor_proficiencies
            assert 'Rapiers' in retrieved_class.weapon_proficiencies

    def test_character_species_class_persistence(self, persistent_test_user, app):
        """
        GIVEN: A Character with Species and CharacterClass relationships
        WHEN: The Character is saved and retrieved from the database
        THEN: All relationships should be preserved
        """
        with app.app_context():
            from project.models import Species, CharacterClass, Character
            
            # Create species
            species = Species(
                name='Halfling',
                ability_score_increases={'dex': 2},
                traits=['Lucky', 'Brave', 'Halfling Nimbleness'],
                languages=['Common', 'Halfling'],
                speed=25,
                size='Small'
            )
            db.session.add(species)
            
            # Create character class
            char_class = CharacterClass(
                name='Rogue',
                hit_die=8,
                primary_ability='Dexterity',
                saving_throw_proficiencies=['Dexterity', 'Intelligence'],
                skill_proficiencies=['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth'],
                armor_proficiencies=['Light Armor'],
                weapon_proficiencies=['Simple Weapons', 'Hand Crossbows', 'Longswords', 'Rapiers', 'Shortswords']
            )
            db.session.add(char_class)
            db.session.flush()
            
            # Create character
            character = Character(
                name='Halfling Rogue',
                species_id=species.id,
                class_id=char_class.id,                level=3,
                strength=10,
                dexterity=16,
                constitution=14,
                intelligence=12,
                wisdom=13,
                charisma=8,
                user_id=persistent_test_user.id
            )
            db.session.add(character)
            db.session.commit()
            
            # Retrieve character with relationships
            retrieved_character = Character.query.filter_by(name='Halfling Rogue').first()
            
            assert retrieved_character is not None
            assert retrieved_character.name == 'Halfling Rogue'
            assert retrieved_character.species is not None
            assert retrieved_character.species.name == 'Halfling'
            assert retrieved_character.char_class is not None
            assert retrieved_character.char_class.name == 'Rogue'
            assert retrieved_character.level == 3
            assert retrieved_character.dexterity == 16


@pytest.mark.skip(reason="Testing features in development - Species/CharacterClass models")
@pytest.mark.functional
class TestCharacterLifecycleWithSpeciesClass:
    """Test character lifecycle operations with Species and CharacterClass."""

    def test_character_creation_with_species_class(self, character_lifecycle_setup, app):
        """
        GIVEN: CharacterLifecycle setup with Species and CharacterClass
        WHEN: A character is created with species and class
        THEN: The character should be properly created with all relationships
        """
        with app.app_context():
            from project.models import Species, CharacterClass
            
            lifecycle = character_lifecycle_setup
            
            # Create species
            species = Species(
                name='Tiefling',
                ability_score_increases={'int': 1, 'cha': 2},
                traits=['Darkvision', 'Hellish Resistance', 'Infernal Legacy'],
                languages=['Common', 'Infernal'],
                speed=30,
                size='Medium'
            )
            db.session.add(species)
            db.session.flush()
            
            # Create character class
            char_class = CharacterClass(
                name='Warlock',
                hit_die=8,
                primary_ability='Charisma',
                saving_throw_proficiencies=['Wisdom', 'Charisma'],
                skill_proficiencies=['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion'],
                armor_proficiencies=['Light Armor'],
                weapon_proficiencies=['Simple Weapons']
            )
            db.session.add(char_class)
            db.session.flush()
            
            # Create character using lifecycle
            character = lifecycle.create_character(
                name='Tiefling Warlock',                species_id=species.id,
                class_id=char_class.id,
                level=1,
                strength=10,
                dexterity=14,
                constitution=12,
                intelligence=13,
                wisdom=8,
                charisma=15
            )
            
            # Verify character creation
            assert character.name == 'Tiefling Warlock'
            assert character.species.name == 'Tiefling'
            assert character.char_class.name == 'Warlock'
            assert character.level == 1
            assert character.charisma == 15

    def test_character_level_up_with_species_class(self, character_lifecycle_setup, app):
        """
        GIVEN: A character with Species and CharacterClass
        WHEN: The character levels up
        THEN: The character should maintain all relationships after level up
        """
        with app.app_context():
            from project.models import Species, CharacterClass
            
            lifecycle = character_lifecycle_setup
            
            # Create species
            species = Species(
                name='Dwarf',
                ability_score_increases={'con': 2},
                traits=['Darkvision', 'Dwarven Resilience', 'Stonecunning'],
                languages=['Common', 'Dwarvish'],
                speed=25,
                size='Medium'
            )
            db.session.add(species)
            db.session.flush()
            
            # Create character class
            char_class = CharacterClass(
                name='Fighter',
                hit_die=10,
                primary_ability='Strength',
                saving_throw_proficiencies=['Strength', 'Constitution'],
                skill_proficiencies=['Acrobatics', 'Animal Handling', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival'],
                armor_proficiencies=['Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields'],
                weapon_proficiencies=['Simple Weapons', 'Martial Weapons']
            )
            db.session.add(char_class)
            db.session.flush()
            
            # Create character
            character = lifecycle.create_character(
                name='Dwarf Fighter',                species_id=species.id,
                class_id=char_class.id,
                level=1,
                strength=15,
                dexterity=12,
                constitution=14,
                intelligence=10,
                wisdom=13,
                charisma=8
            )
            
            # Level up character
            lifecycle.level_up_character(character, new_level=2)
            
            # Verify relationships are maintained after level up
            assert character.level == 2
            assert character.species is not None
            assert character.species.name == 'Dwarf'
            assert character.char_class is not None
            assert character.char_class.name == 'Fighter'
            assert character.proficiency_bonus == 2  # Should be updated
