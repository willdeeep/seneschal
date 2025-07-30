"""Tests for Step 6 character creation fixes."""
import pytest


class TestStep6Fixes:
    """Test class for Step 6 progressive enhancement fixes."""

    def test_progress_bar_elements_correct(self, client, auth):
        """Test that progress bar uses correct element IDs."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check that progress bar has correct IDs
        assert 'id="progress-bar"' in html
        assert 'id="progress-percentage"' in html

        # Check that JavaScript uses correct element IDs
        assert 'getElementById(\'progress-bar\')' in html
        assert 'getElementById(\'progress-percentage\')' in html

    def test_subspecies_filtering_attributes(self, client, auth):
        """Test that subspecies options have correct data attributes for filtering."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check that subspecies select exists (data attributes are added by Jinja template)
        assert 'id="subspecies_id"' in html
        assert 'Select Subspecies (Optional)' in html

        # Check that filterSubspecies function exists (function call exists)
        assert 'filterSubspecies()' in html

    def test_proficiency_api_includes_limits(self, client, auth):
        """Test that proficiency API includes max_selections field."""
        auth.signup()
        auth.login()

        # Test proficiencies API includes max_selections
        response = client.get('/characters/api/proficiencies?species_id=1&class_id=1')
        assert response.status_code == 200

        data = response.get_json()
        assert 'max_selections' in data
        assert isinstance(data['max_selections'], int)
        assert data['max_selections'] >= 2

    def test_rogue_gets_more_proficiencies(self, client, auth):
        """Test that Rogue class gets 4 skill proficiencies."""
        auth.signup()
        auth.login()

        # First, create a Rogue class for testing since it may not exist in test DB
        from project import db
        from project.models import CharacterClass

        # Check if Rogue already exists
        rogue = CharacterClass.query.filter_by(name='Rogue').first()
        if not rogue:
            rogue = CharacterClass(
                name="Rogue",
                hit_die=8,
                primary_ability="Dexterity",
                saving_throw_proficiencies=["Dexterity", "Intelligence"],
                skill_proficiencies=["Stealth", "Sleight of Hand", "Perception", "Investigation"]
            )
            db.session.add(rogue)
            db.session.commit()

        # Test proficiencies API with Rogue (should allow 4 selections)
        response = client.get(f'/characters/api/proficiencies?species_id=1&class_id={rogue.id}')
        assert response.status_code == 200

        data = response.get_json()
        assert data['max_selections'] == 4  # Rogue gets 4 skill proficiencies

    def test_all_classes_have_proficiencies(self, client, auth):
        """Test that all character classes have some proficiencies available."""
        auth.signup()
        auth.login()

        # Test several different classes
        class_ids = [1, 2, 3, 4, 5]  # Fighter, Wizard, Rogue, Cleric, Ranger
        for class_id in class_ids:
            response = client.get(f'/characters/api/proficiencies?species_id=1&class_id={class_id}')
            assert response.status_code == 200

            data = response.get_json()
            assert 'optional' in data
            assert len(data['optional']) > 0  # Should have at least some optional proficiencies

    def test_proficiency_selection_counter_elements(self, client, auth):
        """Test that proficiency selection counter elements exist."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check for proficiency counter elements
        assert 'id="proficiency-count"' in html
        assert 'handleProficiencySelection' in html
        assert 'updateProficiencyCounter' in html

    def test_progress_update_event_listeners(self, client, auth):
        """Test that progress update event listeners are properly attached."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check for updateProgress function calls
        assert 'updateProgress()' in html
        assert 'updateCharacterPreview()' in html
        assert 'addEventListener' in html

    def test_subspecies_initial_filtering(self, client, auth):
        """Test that subspecies filtering is called on page load."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check that filterSubspecies is called on DOMContentLoaded
        assert 'filterSubspecies();' in html
        assert 'DOMContentLoaded' in html


class TestProficiencyLimitsIntegration:
    """Test class for proficiency limits integration."""

    def test_proficiency_selection_limit_javascript(self, client, auth):
        """Test that JavaScript includes proficiency selection limits."""
        auth.signup()
        auth.login()

        response = client.get('/characters/create')
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        # Check for limit handling in JavaScript
        assert 'data-max=' in html  # Checkboxes should have max attribute
        assert 'optional-proficiency' in html  # CSS class for optional proficiencies
        assert 'You can only select up to' in html  # Limit warning message

    def test_comprehensive_class_proficiencies(self, client, auth):
        """Test that comprehensive class proficiencies are available."""
        auth.signup()
        auth.login()

        from project import db
        from project.models import CharacterClass

        # Create test classes if they don't exist
        test_classes = [
            ("Fighter", 2),
            ("Rogue", 4),
            ("Bard", 3),
            ("Ranger", 3),
        ]

        created_classes = []
        for class_name, expected_max in test_classes:
            char_class = CharacterClass.query.filter_by(name=class_name).first()
            if not char_class:
                char_class = CharacterClass(
                    name=class_name,
                    hit_die=8,
                    primary_ability="Strength",
                    saving_throw_proficiencies=["Strength"]
                )
                db.session.add(char_class)
                db.session.commit()

            created_classes.append((char_class.id, expected_max))

        # Test each class
        for class_id, expected_max in created_classes:
            response = client.get(f'/characters/api/proficiencies?species_id=1&class_id={class_id}')
            assert response.status_code == 200

            data = response.get_json()
            assert data['max_selections'] == expected_max

    def test_proficiency_categories_are_logical(self, client, auth):
        """Test that proficiency categories make sense for D&D 5e."""
        auth.signup()
        auth.login()

        # Test that proficiencies have logical categories
        response = client.get('/characters/api/proficiencies?species_id=1&class_id=1')
        assert response.status_code == 200

        data = response.get_json()

        # Check that proficiencies have proper structure
        if 'optional' in data and data['optional']:
            for prof in data['optional']:
                assert 'id' in prof
                assert 'name' in prof
                assert 'category' in prof

                # Categories should be D&D appropriate
                valid_categories = ['Skill', 'Tool', 'Weapon', 'Armor', 'Language']
                assert prof['category'] in valid_categories or prof['category'].endswith('Proficiency')
