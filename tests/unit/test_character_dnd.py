"""
Test cases specifically for D&D character functionality.
Demonstrates proper test marking for CI/local environments.
"""

import pytest
from project.models import Character
from project import db


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

    def test_character_creation_and_persistence(self, app, persistent_test_user):
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
                user_id=persistent_test_user.id
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
            
            # Cleanup
            db.session.delete(saved_character)
            db.session.commit()

    def test_character_relationships(self, app, persistent_test_user):
        """Test character relationships with proficiencies and languages."""
        with app.app_context():
            # Create test data using persistent user
            from project.models import Character, Proficiency, Language
            from project import db
            
            # Create test character
            character = Character(
                name="Test Character",
                race="Human",
                character_class="Fighter",
                level=1,
                strength=15,
                dexterity=14,
                constitution=13,
                intelligence=12,
                wisdom=10,
                charisma=8,
                user_id=persistent_test_user.id
            )
            db.session.add(character)

            # Create test proficiencies
            athletics = Proficiency(
                name="Athletics",
                proficiency_type="skill",
                associated_ability="strength"
            )
            longswords = Proficiency(
                name="Longswords",
                proficiency_type="weapon"
            )
            db.session.add_all([athletics, longswords])

            # Create test language
            common = Language(name="Common", language_type="Standard")
            db.session.add(common)
            
            db.session.commit()

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
            
            # Cleanup test data
            character.proficiencies.clear()
            character.languages.clear()
            db.session.delete(character)
            db.session.delete(athletics)
            db.session.delete(longswords)
            db.session.delete(common)
            db.session.commit()


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

    def test_backstory_persistence(self, persistent_test_user, app):
        """Test that backstory fields persist in database using session-scoped fixtures."""
        with app.app_context():
            # Use the persistent test user that stays attached to session
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
                user_id=persistent_test_user.id  # No DetachedInstanceError!
            )

            db.session.add(character)
            db.session.commit()
            character_id = character.id

            # Clear session and reload to test true persistence
            db.session.expunge(character)
            reloaded_character = db.session.get(Character, character_id)

            # Verify all backstory fields persisted correctly
            assert reloaded_character.why_adventuring == "Forest was destroyed by industry"
            assert reloaded_character.motivation == "Environmental protection, justice"
            assert reloaded_character.origin == "Ancient forest grove"

            # Clean up the character we created
            db.session.delete(reloaded_character)
            db.session.commit()

    def test_backstory_workflow_with_lifecycle(self, character_lifecycle_setup):
        """Test complete backstory development workflow using lifecycle fixture."""
        lifecycle = character_lifecycle_setup

        # Step 1: Create character with initial backstory
        character = lifecycle.create_character(
            name="Evolving Hero",
            race="Human",
            character_class="Paladin",
            why_adventuring="Seeking redemption for past sins",
            motivation="Honor, justice",
            origin="Fallen noble house",
            class_origin="Divine calling after tragedy",
            attachments="Family heirloom sword",
            secret="Responsible for family's downfall",
            attitude_origin="Stoic determination masking guilt"
        )

        # Verify initial backstory
        assert character.why_adventuring == "Seeking redemption for past sins"
        assert character.secret == "Responsible for family's downfall"

        # Step 2: Character grows and backstory evolves (level 5)
        character = lifecycle.level_up_character(character, 5)

        # Update backstory as character develops
        character.motivation += ", protecting others"
        character.secret = "Learning to forgive themselves"
        db.session.commit()

        # Step 3: Major character development (level 10)
        character = lifecycle.level_up_character(character, 10)

        # Backstory continues to evolve
        character.why_adventuring = "Now seeks to help others find redemption"
        character.attitude_origin = "Wise mentor who has overcome past trauma"
        db.session.commit()

        # Step 4: Verify character development persisted across all operations
        saved_character = Character.query.filter_by(name="Evolving Hero").first()
        assert saved_character.level == 10
        assert saved_character.proficiency_bonus == 4
        assert "help others find redemption" in saved_character.why_adventuring
        assert "protecting others" in saved_character.motivation
        assert saved_character.secret == "Learning to forgive themselves"
        assert "Wise mentor" in saved_character.attitude_origin


@pytest.mark.unit
class TestAdvancedCharacterScenarios:
    """Advanced testing scenarios enabled by session-scoped fixtures."""

    def test_character_progression_workflow(self, character_lifecycle_setup):
        """Test complete character progression from creation to high level."""
        lifecycle = character_lifecycle_setup

        # Step 1: Create a new character
        character = lifecycle.create_character(
            name="Aragorn",
            race="Human",
            character_class="Ranger"
        )
        assert character.level == 1
        assert character.proficiency_bonus == 2

        # Step 2: Level up multiple times
        character = lifecycle.level_up_character(character, 5)
        assert character.level == 5
        assert character.proficiency_bonus == 3

        character = lifecycle.level_up_character(character, 11)
        assert character.level == 11
        assert character.proficiency_bonus == 4

        # Step 3: Verify character persists across operations
        saved_character = Character.query.filter_by(name="Aragorn").first()
        assert saved_character.level == 11
        assert saved_character.proficiency_bonus == 4

    def test_party_dynamics_and_balance(self, campaign_party_setup):
        """Test party composition and balance calculations."""
        party = campaign_party_setup

        # Verify party roles are properly distributed
        assert party['tank'].character_class == 'Paladin'
        assert party['dps'].character_class == 'Ranger'
        assert party['healer'].character_class == 'Cleric'
        assert party['utility'].character_class == 'Rogue'

        # Test party-wide statistics
        total_levels = sum(char.level for char in party.values())
        assert total_levels == 12  # 4 characters at level 3

        # Test role-specific abilities
        assert party['tank'].strength >= 15  # Tank needs high STR
        assert party['dps'].dexterity >= 16   # DPS needs high DEX
        assert party['healer'].wisdom >= 15   # Healer needs high WIS
        assert party['utility'].dexterity >= 17  # Rogue needs highest DEX

        # Test that all characters belong to same user
        user_ids = {char.user_id for char in party.values()}
        assert len(user_ids) == 1  # All same user

    def test_complex_character_relationships(self, character_lifecycle_setup, app):
        """Test complex character relationships and dependencies."""
        lifecycle = character_lifecycle_setup

        with app.app_context():
            # Create a mentor character
            mentor = lifecycle.create_character(
                name="Gandalf the Grey",
                race="Human",
                character_class="Wizard",
                level=20
            )

            # Create a student character
            student = lifecycle.create_character(
                name="Frodo Baggins",
                race="Halfling",
                character_class="Rogue",
                level=1
            )

            # In a real application, you might have mentor relationships
            # This demonstrates how session-scoped fixtures enable complex testing

            # Verify both characters exist and can be queried together
            characters = Character.query.filter(
                Character.name.in_(['Gandalf the Grey', 'Frodo Baggins'])
            ).all()
            assert len(characters) == 2

            # Test level difference calculations (for mentorship mechanics)
            level_diff = mentor.level - student.level
            assert level_diff == 19

            # Future: Test mentor bonuses, experience sharing, etc.

    def test_character_data_integrity_across_operations(self, persistent_test_user, app):
        """Test that character data remains consistent across multiple operations."""
        with app.app_context():
            # Create character with complex backstory
            character = Character(
                name="Complex Character",
                race="Half-Elf",
                character_class="Bard",
                level=5,
                strength=12, dexterity=16, constitution=14,
                intelligence=13, wisdom=12, charisma=18,
                # Complex backstory fields
                why_adventuring="Seeking lost family heritage",
                motivation="Family, knowledge, fame",
                origin="Noble court raised by servants",
                class_origin="Self-taught musical prodigy",
                attachments="Father's lute, family signet ring",
                secret="Actually heir to overthrown kingdom",
                attitude_origin="Charming exterior hiding deep insecurity",
                user_id=persistent_test_user.id
            )

            db.session.add(character)
            db.session.commit()
            character_id = character.id

            # Perform multiple operations
            character.level = 6
            character.update_proficiency_bonus()
            db.session.commit()

            # Modify backstory
            character.motivation += ", justice"
            character.secret = "Recently discovered royal heritage"
            db.session.commit()

            # Clear session and reload to test persistence
            db.session.expunge(character)
            reloaded = db.session.get(Character, character_id)

            # Verify all data persisted correctly
            assert reloaded.level == 6
            assert reloaded.proficiency_bonus == 3
            assert "justice" in reloaded.motivation
            assert "Recently discovered" in reloaded.secret
            assert reloaded.attachments == "Father's lute, family signet ring"
