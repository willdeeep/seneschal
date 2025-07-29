"""
Test cases for enhanced character creation UI functionality.
Tests dynamic species/class selection, ability score calculations, and form interactions.
"""

import pytest
import json
from project.models import Species, CharacterClass, SubSpecies
from project import db


@pytest.mark.functional
class TestCharacterCreationUI:
    """Test the enhanced character creation interface."""

    def test_character_creation_page_loads_with_data(self, client, auth, test_user):
        """Test that character creation page loads with species and class data."""
        # Login first
        auth.login()

        # Create test data
        with client.application.app_context():
            species = Species(
                name="Test Elf",
                ability_score_increases={"dex": 2},
                traits=["Darkvision"],
                languages=["Common", "Elvish"],
                speed=30,
                size="Medium"
            )
            char_class = CharacterClass(
                name="Test Ranger",
                hit_die=10,
                primary_ability="Dexterity",
                saving_throw_proficiencies=["Strength", "Dexterity"],
                skill_proficiencies=["Animal Handling", "Athletics"],
                armor_proficiencies=["Light Armor", "Medium Armor"],
                weapon_proficiencies=["Simple Weapons", "Martial Weapons"]
            )
            db.session.add_all([species, char_class])
            db.session.commit()

            species_id = species.id
            class_id = char_class.id

        # Test character creation page
        response = client.get('/characters/create')
        assert response.status_code == 200

        # Check that species and class data is in the response
        response_text = response.get_data(as_text=True)
        assert "Test Elf" in response_text
        assert "Test Ranger" in response_text
        assert 'id="species_id"' in response_text
        assert 'id="class_id"' in response_text
        assert 'id="subspecies_id"' in response_text

        # Cleanup
        with client.application.app_context():
            db.session.delete(db.session.get(Species, species_id))
            db.session.delete(db.session.get(CharacterClass, class_id))
            db.session.commit()

    def test_ability_bonuses_api_endpoint(self, client, auth, test_user):
        """Test the ability bonuses API endpoint."""
        # Login first
        auth.login()

        # Create test species with ability bonuses
        with client.application.app_context():
            species = Species(
                name="Test Dragonborn",
                ability_score_increases={"str": 2, "cha": 1},
                traits=["Draconic Ancestry", "Breath Weapon"],
                languages=["Common", "Draconic"],
                speed=30,
                size="Medium"
            )
            subspecies = SubSpecies(
                name="Red Dragonborn",
                species=species,
                additional_traits=["Fire Resistance"]
            )
            db.session.add_all([species, subspecies])
            db.session.commit()

            species_id = species.id
            subspecies_id = subspecies.id

        # Test API endpoint without subspecies
        response = client.get(f'/characters/ability-bonuses?species_id={species_id}')
        assert response.status_code == 200

        data = json.loads(response.get_data(as_text=True))
        assert 'bonuses' in data
        assert data['bonuses']['str'] == 2
        assert data['bonuses']['cha'] == 1
        assert data['bonuses']['dex'] == 0  # Should default to 0
        assert 'species_info' in data
        assert data['species_info']['speed'] == 30

        # Test API endpoint with subspecies
        response = client.get(f'/characters/ability-bonuses?species_id={species_id}&subspecies_id={subspecies_id}')
        assert response.status_code == 200

        data = json.loads(response.get_data(as_text=True))
        assert 'bonuses' in data
        assert data['bonuses']['str'] == 2
        assert data['bonuses']['cha'] == 1

        # Test API endpoint with invalid species
        response = client.get('/characters/ability-bonuses?species_id=99999')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data['bonuses']['str'] == 0
        assert data['bonuses']['dex'] == 0

        # Cleanup
        with client.application.app_context():
            db.session.delete(db.session.get(SubSpecies, subspecies_id))
            db.session.delete(db.session.get(Species, species_id))
            db.session.commit()

    def test_character_creation_form_submission_with_new_fields(self, client, auth, test_user):
        """Test character creation form submission with species_id and class_id."""
        # Login first
        auth.login()

        # Create test data
        with client.application.app_context():
            species = Species(
                name="Test Human",
                ability_score_increases={"str": 1, "dex": 1, "con": 1, "int": 1, "wis": 1, "cha": 1},
                traits=["Extra Language", "Extra Skill"],
                languages=["Common"],
                speed=30,
                size="Medium"
            )
            char_class = CharacterClass(
                name="Test Fighter",
                hit_die=10,
                primary_ability="Strength",
                saving_throw_proficiencies=["Strength", "Constitution"],
                skill_proficiencies=["Athletics", "Intimidation"],
                armor_proficiencies=["All Armor", "Shields"],
                weapon_proficiencies=["Simple Weapons", "Martial Weapons"]
            )
            db.session.add_all([species, char_class])
            db.session.commit()

            species_id = species.id
            class_id = char_class.id

        # Submit character creation form
        response = client.post('/characters/create', data={
            'name': 'Test Enhanced Character',
            'species_id': species_id,
            'class_id': class_id,
            'level': 1,
            'strength': 15,
            'dexterity': 14,
            'constitution': 13,
            'intelligence': 12,
            'wisdom': 10,
            'charisma': 8,
            'max_hp': 11,
            'current_hp': 11,
            'armor_class': 16,
            'speed': 30,
            'initiative': 2,
            'gold_pieces': 150
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b"Character Test Enhanced Character created successfully!" in response.data

        # Verify character was created in database
        with client.application.app_context():
            from project.models import Character
            character = Character.query.filter_by(name='Test Enhanced Character').first()
            assert character is not None
            assert character.species_id == species_id
            assert character.class_id == class_id
            assert character.species.name == "Test Human"
            assert character.char_class.name == "Test Fighter"

            # Cleanup
            db.session.delete(character)
            db.session.delete(db.session.get(Species, species_id))
            db.session.delete(db.session.get(CharacterClass, class_id))
            db.session.commit()

    def test_character_creation_form_validation(self, client, auth, test_user):
        """Test form validation for required fields."""
        # Login first
        auth.login()

        # Test missing required fields
        response = client.post('/characters/create', data={
            'name': 'Incomplete Character',
            # Missing species_id and class_id
            'level': 1,
            'strength': 10
        })

        assert response.status_code == 200
        response_text = response.get_data(as_text=True)
        assert "Species selection is required." in response_text
        assert "Class selection is required." in response_text

    def test_enhanced_form_validation_detailed(self, client, auth, test_user):
        """Test enhanced form validation with detailed error messages."""
        # Login first
        auth.login()
        
        # Test various validation scenarios
        test_cases = [
            {
                'data': {'name': '', 'species_id': '', 'class_id': ''},
                'expected_errors': ['Character name is required.', 'Species selection is required.', 'Class selection is required.']
            },
            {
                'data': {'name': 'A', 'species_id': '1', 'class_id': '1'},
                'expected_errors': ['Character name must be at least 2 characters long.']
            },
            {
                'data': {'name': 'Valid Name', 'species_id': '1', 'class_id': '1', 'strength': '25'},
                'expected_errors': ['Strength must be between 3 and 20.']
            },
            {
                'data': {'name': 'Valid Name', 'species_id': '1', 'class_id': '1', 'max_hp': '0'},
                'expected_errors': ['Maximum HP must be at least 1.']
            },
            {
                'data': {'name': 'Valid Name', 'species_id': '1', 'class_id': '1', 'current_hp': '10', 'max_hp': '5'},
                'expected_errors': ['Current HP cannot exceed Maximum HP.']
            }
        ]
        
        for test_case in test_cases:
            response = client.post('/characters/create', data=test_case['data'])
            assert response.status_code == 200
            response_text = response.get_data(as_text=True)
            
            for expected_error in test_case['expected_errors']:
                assert expected_error in response_text, f"Expected error '{expected_error}' not found in response"

    def test_subspecies_data_in_template(self, client, auth, test_user):
        """Test that subspecies data is properly passed to template."""
        # Login first
        auth.login()

        # Create test data with subspecies
        with client.application.app_context():
            species = Species(
                name="Test Elf Species",
                ability_score_increases={"dex": 2},
                traits=["Darkvision"],
                languages=["Common", "Elvish"],
                speed=30,
                size="Medium"
            )
            subspecies = SubSpecies(
                name="High Elf",
                species=species,
                additional_traits=["Cantrip"]
            )
            db.session.add_all([species, subspecies])
            db.session.commit()

            species_id = species.id
            subspecies_id = subspecies.id

        # Test character creation page
        response = client.get('/characters/create')
        assert response.status_code == 200

        response_text = response.get_data(as_text=True)
        assert "High Elf" in response_text
        assert f'data-species-id="{species_id}"' in response_text

        # Cleanup
        with client.application.app_context():
            db.session.delete(db.session.get(SubSpecies, subspecies_id))
            db.session.delete(db.session.get(Species, species_id))
            db.session.commit()


@pytest.mark.functional
class TestCharacterCreationJavaScript:
    """Test JavaScript functionality in character creation (requires selenium for full testing)."""

    def test_ability_bonuses_api_response_format(self, client, auth, test_user):
        """Test that the ability bonuses API returns properly formatted JSON."""
        # Login first
        auth.login()

        # Create test species
        with client.application.app_context():
            species = Species(
                name="API Test Species",
                ability_score_increases={"str": 2, "wis": 1},
                traits=["Test Trait"],
                languages=["Common"],
                speed=25,
                size="Small"
            )
            db.session.add(species)
            db.session.commit()
            species_id = species.id

        # Test API response format
        response = client.get(f'/characters/ability-bonuses?species_id={species_id}')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.get_data(as_text=True))

        # Check that all required fields are present
        assert 'bonuses' in data
        assert 'species_info' in data

        # Check bonuses structure
        expected_abilities = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        for ability in expected_abilities:
            assert ability in data['bonuses']
            assert isinstance(data['bonuses'][ability], int)

        # Check species info
        assert 'speed' in data['species_info']
        assert 'size' in data['species_info']
        assert 'traits' in data['species_info']
        assert 'languages' in data['species_info']

        # Verify values
        assert data['bonuses']['str'] == 2
        assert data['bonuses']['wis'] == 1
        assert data['bonuses']['dex'] == 0
        assert data['species_info']['speed'] == 25
        assert data['species_info']['size'] == "Small"

        # Cleanup
        with client.application.app_context():
            db.session.delete(db.session.get(Species, species_id))
            db.session.commit()

    def test_api_handles_missing_parameters(self, client, auth, test_user):
        """Test API gracefully handles missing or invalid parameters."""
        # Login first
        auth.login()

        # Test with no parameters
        response = client.get('/characters/ability-bonuses')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))

        # Should return zero bonuses
        expected_abilities = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        for ability in expected_abilities:
            assert data['bonuses'][ability] == 0

        # Test with invalid species_id
        response = client.get('/characters/ability-bonuses?species_id=invalid')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))

        # Should return zero bonuses
        for ability in expected_abilities:
            assert data['bonuses'][ability] == 0


@pytest.mark.unit
class TestAbilityScoreCalculations:
    """Unit tests for ability score calculation logic."""

    def test_modifier_calculation_javascript_equivalent(self):
        """Test that our Python modifier calculation matches JavaScript logic."""
        # This would be the Python equivalent of the JavaScript calculateAbilityModifier function
        def calculate_ability_modifier(score):
            return (score - 10) // 2

        # Test various scores
        test_cases = [
            (1, -5),   # Very low
            (8, -1),   # Below average
            (10, 0),   # Average
            (11, 0),   # Just above average
            (12, 1),   # Above average
            (16, 3),   # High
            (18, 4),   # Very high
            (20, 5),   # Maximum normal
        ]

        for score, expected_modifier in test_cases:
            assert calculate_ability_modifier(score) == expected_modifier

    def test_species_ability_bonus_aggregation(self, app):
        """Test aggregation of ability bonuses from species and subspecies."""
        with app.app_context():
            # Create species with bonuses
            species = Species(
                name="Test Species",
                ability_score_increases={"str": 2, "con": 1},
                traits=["Test"],
                languages=["Common"],
                speed=30,
                size="Medium"
            )

            # Create subspecies with additional bonuses
            subspecies = SubSpecies(
                name="Test Subspecies",
                species=species,
                additional_traits=["Extra Test"]
            )

            db.session.add_all([species, subspecies])
            db.session.flush()

            # Test that bonuses are properly calculated
            # (This would normally be done in the API endpoint)
            base_bonuses = species.ability_score_increases or {}

            expected_bonuses = {
                'str': base_bonuses.get('str', 0),
                'dex': base_bonuses.get('dex', 0),
                'con': base_bonuses.get('con', 0),
                'int': base_bonuses.get('int', 0),
                'wis': base_bonuses.get('wis', 0),
                'cha': base_bonuses.get('cha', 0)
            }

            assert expected_bonuses['str'] == 2
            assert expected_bonuses['con'] == 1
            assert expected_bonuses['dex'] == 0

            # Cleanup
            db.session.rollback()
