"""
Test cases specifically for D&D character functionality.
Demonstrates proper test marking for CI/local environments.
"""

import pytest
from project.models import Character, Species, CharacterClass
from project import db


@pytest.mark.unit
class TestCharacterModelUnit:
    """Unit tests for Character model that don't require database."""

    def test_ability_modifier_calculation(self):
        """Test ability modifier calculation without database."""
        # This doesn't require database, just tests the calculation
        character = Character()

        # Test various ability scores
        assert character.get_ability_modifier(10) == 0  # Average
        assert character.get_ability_modifier(8) == -1  # Below average
        assert character.get_ability_modifier(16) == 3  # High
        assert character.get_ability_modifier(20) == 5  # Max standard
        assert character.get_ability_modifier(3) == -4  # Very low

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
            # Create test species
            species = Species(
                name="Dragonborn",
                ability_score_increases={"str": 2, "cha": 1},
                traits=["Draconic Ancestry", "Breath Weapon", "Damage Resistance"],
                languages=["Common", "Draconic"],
                speed=30,
                size="Medium",
            )
            db.session.add(species)
            db.session.flush()

            # Create test character class
            char_class = CharacterClass(
                name="Paladin",
                hit_die=10,
                primary_ability="Charisma",
                saving_throw_proficiencies=["Wisdom", "Charisma"],
                skill_proficiencies=[
                    "Athletics",
                    "Insight",
                    "Intimidation",
                    "Medicine",
                    "Persuasion",
                    "Religion",
                ],
                armor_proficiencies=[
                    "Light Armor",
                    "Medium Armor",
                    "Heavy Armor",
                    "Shields",
                ],
                weapon_proficiencies=["Simple Weapons", "Martial Weapons"],
            )
            db.session.add(char_class)
            db.session.flush()

            character = Character(
                name="Test Paladin",
                species_id=species.id,
                class_id=char_class.id,
                level=2,
                strength=16,
                dexterity=10,
                constitution=14,
                intelligence=8,
                wisdom=12,
                charisma=15,
                user_id=persistent_test_user.id,
            )

            db.session.add(character)
            db.session.commit()

            # Verify character was saved
            saved_character = Character.query.filter_by(name="Test Paladin").first()
            assert saved_character is not None
            assert saved_character.species.name == "Dragonborn"
            assert saved_character.char_class.name == "Paladin"

            # Cleanup
            db.session.delete(saved_character)
            db.session.delete(species)
            db.session.delete(char_class)
            db.session.commit()

    def test_character_relationships(self, app, persistent_test_user):
        """Test character relationships with proficiencies and languages."""
        with app.app_context():
            # Create test data using persistent user
            from project.models import Character, Proficiency, Language
            from project import db

            # Create test species
            species = Species(
                name="Human",
                ability_score_increases={
                    "str": 1,
                    "dex": 1,
                    "con": 1,
                    "int": 1,
                    "wis": 1,
                    "cha": 1,
                },
                traits=["Extra Language", "Extra Skill"],
                languages=["Common"],
                speed=30,
                size="Medium",
            )
            db.session.add(species)
            db.session.flush()

            # Create test character class
            char_class = CharacterClass(
                name="Fighter",
                hit_die=10,
                primary_ability="Strength",
                saving_throw_proficiencies=["Strength", "Constitution"],
                skill_proficiencies=[
                    "Acrobatics",
                    "Animal Handling",
                    "Athletics",
                    "History",
                    "Insight",
                    "Intimidation",
                    "Perception",
                    "Survival",
                ],
                armor_proficiencies=[
                    "Light Armor",
                    "Medium Armor",
                    "Heavy Armor",
                    "Shields",
                ],
                weapon_proficiencies=["Simple Weapons", "Martial Weapons"],
            )
            db.session.add(char_class)
            db.session.flush()

            # Create test character
            character = Character(
                name="Test Character",
                species_id=species.id,
                class_id=char_class.id,
                level=1,
                strength=15,
                dexterity=14,
                constitution=13,
                intelligence=12,
                wisdom=10,
                charisma=8,
                user_id=persistent_test_user.id,
            )
            db.session.add(character)

            # Create test proficiencies
            athletics = Proficiency(
                name="Athletics",
                proficiency_type="skill",
                associated_ability="strength",
            )
            longswords = Proficiency(name="Longswords", proficiency_type="weapon")
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
            db.session.delete(species)
            db.session.delete(char_class)
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

    def test_random_character_generation(self, app, persistent_test_user):
        """Test generating random characters with all combinations."""
        # This might be slow and is primarily for local testing
        with app.app_context():
            # Create test species
            species_data = [
                {
                    "name": "Human",
                    "ability_score_increases": {
                        "str": 1,
                        "dex": 1,
                        "con": 1,
                        "int": 1,
                        "wis": 1,
                        "cha": 1,
                    },
                },
                {"name": "Elf", "ability_score_increases": {"dex": 2}},
                {"name": "Dwarf", "ability_score_increases": {"con": 2}},
                {"name": "Halfling", "ability_score_increases": {"dex": 2}},
            ]

            species_list = []
            for data in species_data:
                species = Species(
                    name=data["name"],
                    ability_score_increases=data["ability_score_increases"],
                    traits=[],
                    languages=["Common"],
                    speed=30,
                    size="Medium",
                )
                db.session.add(species)
                species_list.append(species)

            # Create test character classes
            class_data = [
                {"name": "Fighter", "hit_die": 10, "primary_ability": "Strength"},
                {"name": "Wizard", "hit_die": 6, "primary_ability": "Intelligence"},
                {"name": "Rogue", "hit_die": 8, "primary_ability": "Dexterity"},
                {"name": "Cleric", "hit_die": 8, "primary_ability": "Wisdom"},
            ]

            class_list = []
            for data in class_data:
                char_class = CharacterClass(
                    name=data["name"],
                    hit_die=data["hit_die"],
                    primary_ability=data["primary_ability"],
                    saving_throw_proficiencies=[],
                    skill_proficiencies=[],
                    armor_proficiencies=[],
                    weapon_proficiencies=[],
                )
                db.session.add(char_class)
                class_list.append(char_class)

            db.session.flush()

            characters_created = 0
            for species in species_list:
                for char_class in class_list:
                    character = Character(
                        name=f"Test {species.name} {char_class.name}",
                        species_id=species.id,
                        class_id=char_class.id,
                        level=1,
                        strength=13,
                        dexterity=14,
                        constitution=12,
                        intelligence=10,
                        wisdom=15,
                        charisma=8,
                        user_id=persistent_test_user.id,
                    )

                    db.session.add(character)
                    characters_created += 1

            db.session.commit()
            assert characters_created == len(species_list) * len(class_list)


@pytest.mark.unit
class TestCharacterBackstoryFields:
    """Test the enhanced backstory fields added to the Character model."""

    def test_backstory_field_assignment(self, app):
        """Test that all backstory fields can be assigned."""
        with app.app_context():
            # Create test species
            species = Species(
                name="Human",
                ability_score_increases={
                    "str": 1,
                    "dex": 1,
                    "con": 1,
                    "int": 1,
                    "wis": 1,
                    "cha": 1,
                },
                traits=["Extra Language", "Extra Skill"],
                languages=["Common"],
                speed=30,
                size="Medium",
            )
            db.session.add(species)

            # Create test character class
            char_class = CharacterClass(
                name="Fighter",
                hit_die=10,
                primary_ability="Strength",
                saving_throw_proficiencies=[],
                skill_proficiencies=[],
                armor_proficiencies=[],
                weapon_proficiencies=[],
            )
            db.session.add(char_class)
            db.session.flush()

            character = Character(
                name="Backstory Test Character",
                species_id=species.id,
                class_id=char_class.id,
                strength=15,
                dexterity=14,
                constitution=13,
                intelligence=12,
                wisdom=10,
                charisma=8,
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
            # Create test species
            species = Species(
                name="Elf",
                ability_score_increases={"dex": 2},
                traits=["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"],
                languages=["Common", "Elvish"],
                speed=30,
                size="Medium",
            )
            db.session.add(species)

            # Create test character class
            char_class = CharacterClass(
                name="Ranger",
                hit_die=10,
                primary_ability="Dexterity",
                saving_throw_proficiencies=[],
                skill_proficiencies=[],
                armor_proficiencies=[],
                weapon_proficiencies=[],
            )
            db.session.add(char_class)
            db.session.flush()

            # Use the persistent test user that stays attached to session
            character = Character(
                name="Persistent Backstory Character",
                species_id=species.id,
                class_id=char_class.id,
                level=1,
                strength=13,
                dexterity=16,
                constitution=14,
                intelligence=12,
                wisdom=15,
                charisma=8,
                why_adventuring="Forest was destroyed by industry",
                motivation="Environmental protection, justice",
                origin="Ancient forest grove",
                user_id=persistent_test_user.id,  # No DetachedInstanceError!
            )

            db.session.add(character)
            db.session.commit()
            character_id = character.id

            # Clear session and reload to test true persistence
            db.session.expunge(character)
            reloaded_character = db.session.get(Character, character_id)

            # Verify all backstory fields persisted correctly
            assert (
                reloaded_character.why_adventuring == "Forest was destroyed by industry"
            )
            assert reloaded_character.motivation == "Environmental protection, justice"
            assert reloaded_character.origin == "Ancient forest grove"

            # Clean up the character we created
            species_to_delete = reloaded_character.species
            char_class_to_delete = reloaded_character.char_class
            db.session.delete(reloaded_character)
            db.session.delete(species_to_delete)
            db.session.delete(char_class_to_delete)
            db.session.commit()

    def test_backstory_workflow_with_lifecycle(self, character_lifecycle_setup):
        """Test complete backstory development workflow using lifecycle fixture."""
        lifecycle = character_lifecycle_setup

        # Step 1: Create character with initial backstory
        character = lifecycle.create_character(
            name="Evolving Hero",
            species="Human",
            character_class="Paladin",
            why_adventuring="Seeking redemption for past sins",
            motivation="Honor, justice",
            origin="Fallen noble house",
            class_origin="Divine calling after tragedy",
            attachments="Family heirloom sword",
            secret="Responsible for family's downfall",
            attitude_origin="Stoic determination masking guilt",
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
            name="Aragorn", species="Human", character_class="Ranger"
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
        assert party["tank"].char_class.name == "Paladin"
        assert party["dps"].char_class.name == "Ranger"
        assert party["healer"].char_class.name == "Cleric"
        assert party["utility"].char_class.name == "Rogue"

        # Test party-wide statistics
        total_levels = sum(char.level for char in party.values())
        assert total_levels == 12  # 4 characters at level 3

        # Test role-specific abilities
        assert party["tank"].strength >= 15  # Tank needs high STR
        assert party["dps"].dexterity >= 16  # DPS needs high DEX
        assert party["healer"].wisdom >= 15  # Healer needs high WIS
        assert party["utility"].dexterity >= 17  # Rogue needs highest DEX

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
                species="Human",
                character_class="Wizard",
                level=20,
            )

            # Create a student character
            student = lifecycle.create_character(
                name="Frodo Baggins",
                species="Halfling",
                character_class="Rogue",
                level=1,
            )

            # In a real application, you might have mentor relationships
            # This demonstrates how session-scoped fixtures enable complex
            # testing

            # Verify both characters exist and can be queried together
            characters = Character.query.filter(
                Character.name.in_(["Gandalf the Grey", "Frodo Baggins"])
            ).all()
            assert len(characters) == 2

            # Test level difference calculations (for mentorship mechanics)
            level_diff = mentor.level - student.level
            assert level_diff == 19

            # Future: Test mentor bonuses, experience sharing, etc.

    def test_character_data_integrity_across_operations(
        self, persistent_test_user, app
    ):
        """Test that character data remains consistent across multiple operations."""
        with app.app_context():
            # Create test species
            species = Species(
                name="Half-Elf",
                ability_score_increases={"cha": 2, "str": 1, "dex": 1},
                traits=["Darkvision", "Fey Ancestry", "Skill Versatility"],
                languages=["Common", "Elvish"],
                speed=30,
                size="Medium",
            )
            db.session.add(species)

            # Create test character class
            char_class = CharacterClass(
                name="Bard",
                hit_die=8,
                primary_ability="Charisma",
                saving_throw_proficiencies=[],
                skill_proficiencies=[],
                armor_proficiencies=[],
                weapon_proficiencies=[],
            )
            db.session.add(char_class)
            db.session.flush()

            # Create character with complex backstory
            character = Character(
                name="Complex Character",
                species_id=species.id,
                class_id=char_class.id,
                level=5,
                strength=12,
                dexterity=16,
                constitution=14,
                intelligence=13,
                wisdom=12,
                charisma=18,
                # Complex backstory fields
                why_adventuring="Seeking lost family heritage",
                motivation="Family, knowledge, fame",
                origin="Noble court raised by servants",
                class_origin="Self-taught musical prodigy",
                attachments="Father's lute, family signet ring",
                secret="Actually heir to overthrown kingdom",
                attitude_origin="Charming exterior hiding deep insecurity",
                user_id=persistent_test_user.id,
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
