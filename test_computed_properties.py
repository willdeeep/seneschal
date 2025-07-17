"""
Quick test for computed properties functionality
"""

import pytest
from project.models import Character, Species, CharacterClass, db
from project import create_app


def test_computed_properties():
    """Test the computed properties work correctly."""
    app = create_app()

    with app.app_context():
        # Create a Species
        species = Species(
            name="Elf",
            ability_score_increases={"dex": 2},
            traits=["Darkvision", "Keen Senses"],
            languages=["Common", "Elvish"],
            proficiencies=["Perception"],
            speed=30,
            size="Medium",
        )
        db.session.add(species)
        db.session.flush()

        # Create a CharacterClass
        char_class = CharacterClass(
            name="Wizard",
            hit_die=6,
            primary_ability="Intelligence",
            saving_throw_proficiencies=["Intelligence", "Wisdom"],
            skill_proficiencies=["Arcana", "History"],
            armor_proficiencies=[],
            weapon_proficiencies=["Daggers", "Darts"],
        )
        db.session.add(char_class)
        db.session.flush()

        # Create a Character with species and class
        character = Character(
            name="Test Elf Wizard",
            species_id=species.id,
            class_id=char_class.id,
            level=1,
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=15,
            wisdom=13,
            charisma=10,
            user_id=1,  # dummy user ID
        )
        db.session.add(character)
        db.session.flush()

        # Test computed properties
        print(f"Effective ability scores: {character.effective_ability_scores}")
        print(f"All proficiencies: {character.all_proficiencies}")
        print(f"All languages: {character.all_languages}")
        print(f"All traits: {character.all_traits}")
        print(f"Effective speed: {character.effective_speed}")
        print(f"Effective size: {character.effective_size}")

        # Verify the computed properties
        # 14 + 2 from Elf
        assert character.effective_ability_scores["dex"] == 16
        # Base intelligence
        assert character.effective_ability_scores["int"] == 15
        assert "Perception" in character.all_proficiencies
        assert "Arcana" in character.all_proficiencies
        assert "Common" in character.all_languages
        assert "Elvish" in character.all_languages
        assert "Darkvision" in character.all_traits
        assert character.effective_speed == 30
        assert character.effective_size == "Medium"

        print("All computed properties work correctly!")


if __name__ == "__main__":
    test_computed_properties()
