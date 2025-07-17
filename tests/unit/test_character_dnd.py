"""
Test cases specifically for D&D character functionality.
Demonstrates proper test marking for CI/local environments.
"""

import pytest
from project.models import Character


@pytest.mark.unit
class TestCharacterModelUnit:
    """Unit tests for Character model that don't require database."""

    def test_ability_modifier_calculation(self):
        """Test ability modifier calculation without database."""
        # This doesn't require database, just tests the calculation
        character = Character()

        # Test various ability scores
        assert character.get_ability_modifier(10) == 0   # Average
        assert character.get_ability_modifier(8) == -1   # Below average
        assert character.get_ability_modifier(16) == 3   # High
        assert character.get_ability_modifier(20) == 5   # Max standard
        assert character.get_ability_modifier(3) == -4   # Very low

    def test_proficiency_bonus_by_level(self):
        """Test proficiency bonus calculation by level."""
        character = Character()

        # Test level 1-4
        character.level = 1
        character.update_proficiency_bonus()
        assert character.proficiency_bonus == 2

        # Test level 5-8
        character.level = 5
        character.update_proficiency_bonus()
        assert character.proficiency_bonus == 3

        # Test level 9-12
        character.level = 10
        character.update_proficiency_bonus()
        assert character.proficiency_bonus == 4

        # Test level 17+
        character.level = 20
        character.update_proficiency_bonus()
        assert character.proficiency_bonus == 6


@pytest.mark.functional
class TestCharacterModelDatabase:
    """Functional tests that require database interaction."""

    def test_character_creation_and_persistence(self, app, test_user):
        """Test creating and saving a character to database."""
        with app.app_context():
            character = Character(
                name="Test Paladin",
                race="Dragonborn",
                character_class="Paladin",
                level=2,
                strength=16,
                dexterity=10,
                constitution=14,
                intelligence=8,
                wisdom=12,
                charisma=15,
                user_id=test_user.id
            )

            from project import db
            db.session.add(character)
            db.session.commit()

            # Verify character was saved
            saved_character = Character.query.filter_by(
                name="Test Paladin").first()
            assert saved_character is not None
            assert saved_character.race == "Dragonborn"
            assert saved_character.character_class == "Paladin"

    def test_character_relationships(self, app, populated_db):
        """Test character relationships with proficiencies and languages."""
        with app.app_context():
            character = populated_db['character']
            # Athletics proficiency
            athletics = populated_db['proficiencies'][0]
            common = populated_db['languages'][0]  # Common language

            # Add relationships
            character.proficiencies.append(athletics)
            character.languages.append(common)

            from project import db
            db.session.commit()

            # Verify relationships
            assert athletics in character.proficiencies
            assert common in character.languages
            assert character in athletics.characters
            assert character in common.characters


@pytest.mark.requires_db
@pytest.mark.local_only  # This will be skipped in CI
class TestCharacterWithRealDatabase:
    """Tests that require a real PostgreSQL database (local dev only)."""

    def test_complex_character_queries(self, app):
        """Test complex database queries that might not work with SQLite."""
        # This test would only run in local development
        # where you have a real PostgreSQL instance
        pytest.skip("Real database tests not implemented yet")


@pytest.mark.requires_network
@pytest.mark.github_skip  # Explicitly skip in GitHub Actions
class TestD20SRDIntegration:
    """Tests that require network access to D20 SRD API."""

    def test_spell_data_import(self):
        """Test importing spell data from D20 SRD."""
        # This would require network access
        pytest.skip("Network-dependent test - implement when needed")


@pytest.mark.slow
@pytest.mark.local_only
class TestCharacterGeneration:
    """Slow tests for character generation that are local-only."""

    def test_random_character_generation(self, app, populated_db):
        """Test generating random characters with all combinations."""
        # This might be slow and is primarily for local testing
        with app.app_context():
            races = ["Human", "Elf", "Dwarf", "Halfling"]
            classes = ["Fighter", "Wizard", "Rogue", "Cleric"]

            characters_created = 0
            for race in races:
                for char_class in classes:
                    character = Character(
                        name=f"Test {race} {char_class}",
                        race=race,
                        character_class=char_class,
                        level=1,
                        strength=13,
                        dexterity=14,
                        constitution=12,
                        intelligence=10,
                        wisdom=15,
                        charisma=8,
                        user_id=populated_db['user'].id
                    )

                    from project import db
                    db.session.add(character)
                    characters_created += 1

            db.session.commit()
            assert characters_created == len(races) * len(classes)


@pytest.mark.unit
class TestCharacterBackstoryFields:
    """Test the enhanced backstory fields added to the Character model."""

    def test_backstory_field_assignment(self, app):
        """Test that all backstory fields can be assigned."""
        with app.app_context():
            character = Character(
                name="Backstory Test Character",
                race="Human",
                character_class="Fighter",
                strength=15, dexterity=14, constitution=13,
                intelligence=12, wisdom=10, charisma=8
            )

            # Test all backstory fields
            character.why_adventuring = "To seek redemption for past mistakes"
            character.motivation = "Honor, family, redemption"
            character.origin = "Small farming village"
            character.class_origin = "Trained by a retired knight"
            character.attachments = "Younger sister, family sword"
            character.secret = "Was once a deserter"
            character.attitude_origin = "Stoic due to military training"

            # Verify all fields are set
            assert character.why_adventuring is not None
            assert character.motivation is not None
            assert character.origin is not None
            assert character.class_origin is not None
            assert character.attachments is not None
            assert character.secret is not None
            assert character.attitude_origin is not None

    def test_backstory_persistence(self, app, test_user):
        """Test that backstory fields persist in database."""
        with app.app_context():
            character = Character(
                name="Persistent Backstory Character",
                race="Elf",
                character_class="Ranger",
                level=1,
                strength=13, dexterity=16, constitution=14,
                intelligence=12, wisdom=15, charisma=8,
                why_adventuring="Forest was destroyed by industry",
                motivation="Environmental protection, justice",
                origin="Ancient forest grove",
                user_id=test_user.id
            )

            from project import db
            db.session.add(character)
            db.session.commit()
            character_id = character.id

            # Clear session and reload
            db.session.expunge(character)
            reloaded_character = Character.query.get(character_id)

            assert reloaded_character.why_adventuring == "Forest was destroyed by industry"
            assert reloaded_character.motivation == "Environmental protection, justice"
            assert reloaded_character.origin == "Ancient forest grove"
