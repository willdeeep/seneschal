"""Import scraped D&D data into the Seneschal database."""

from project.models import Proficiency, Language, Feature, Item
from project import create_app, db
import json
import logging
import os
import sys
from typing import Dict, List, Any

# Add parent directory to path to import project modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


class DataImporter:
    """Import scraped D&D data into the database."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.app = create_app()

    def load_json_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file."""
        filepath = os.path.join(os.path.dirname(__file__), "data", f"{filename}.json")

        if not os.path.exists(filepath):
            self.logger.warning("File not found: %s", filepath)
            return []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.logger.info("Loaded %d items from %s", len(data), filename)
            return data
        except json.JSONDecodeError as e:
            self.logger.error("Invalid JSON in %s: %s", filename, e)
            return []
        except Exception as e:
            self.logger.error("Error loading %s: %s", filename, e)
            return []

    def import_proficiencies(self, data: List[Dict[str, Any]]) -> int:
        """Import proficiency data."""
        count = 0

        with self.app.app_context():
            for item in data:
                name = item.get("name", "").strip()
                prof_type = item.get("type", "skill").lower()

                if not name:
                    continue

                # Check if already exists
                existing = Proficiency.query.filter_by(name=name).first()
                if existing:
                    continue

                proficiency = Proficiency(name=name, type=prof_type)
                db.session.add(proficiency)
                count += 1

            try:
                db.session.commit()
                self.logger.info("Imported %d new proficiencies", count)
            except Exception as e:
                db.session.rollback()
                self.logger.error("Error importing proficiencies: %s", e)
                count = 0

        return count

    def import_languages(self, data: List[Dict[str, Any]]) -> int:
        """Import language data."""
        count = 0

        with self.app.app_context():
            for item in data:
                name = item.get("name", "").strip()

                if not name:
                    continue

                # Check if already exists
                existing = Language.query.filter_by(name=name).first()
                if existing:
                    continue

                language = Language(name=name)
                db.session.add(language)
                count += 1

            try:
                db.session.commit()
                self.logger.info("Imported %d new languages", count)
            except Exception as e:
                db.session.rollback()
                self.logger.error("Error importing languages: %s", e)
                count = 0

        return count

    def import_features(self, data: List[Dict[str, Any]]) -> int:
        """Import feature data."""
        count = 0

        with self.app.app_context():
            for item in data:
                name = item.get("name", "").strip()
                description = item.get("description", "").strip()
                source = item.get("source", "Unknown").strip()

                if not name or not description:
                    continue

                # Check if already exists
                existing = Feature.query.filter_by(name=name).first()
                if existing:
                    continue

                feature = Feature(name=name, description=description, source=source)
                db.session.add(feature)
                count += 1

            try:
                db.session.commit()
                self.logger.info("Imported %d new features", count)
            except Exception as e:
                db.session.rollback()
                self.logger.error("Error importing features: %s", e)
                count = 0

        return count

    def import_equipment(self, data: List[Dict[str, Any]]) -> int:
        """Import equipment data."""
        count = 0

        with self.app.app_context():
            for item in data:
                name = item.get("name", "").strip()
                item_type = item.get("type", "gear").lower()
                cost = item.get("cost", 0)
                weight = item.get("weight", 0.0)
                description = item.get("description", "").strip()

                if not name:
                    continue

                # Check if already exists
                existing = Item.query.filter_by(name=name).first()
                if existing:
                    continue

                # Convert cost from copper pieces to gold pieces
                cost_gp = max(0, cost // 100) if isinstance(cost, int) else 0

                equipment = Item(
                    name=name,
                    type=item_type,
                    cost_gp=cost_gp,
                    weight_lbs=float(weight) if weight else 0.0,
                    description=description,
                )
                db.session.add(equipment)
                count += 1

            try:
                db.session.commit()
                self.logger.info("Imported %d new equipment items", count)
            except Exception as e:
                db.session.rollback()
                self.logger.error("Error importing equipment: %s", e)
                count = 0

        return count

    def extract_skills_from_data(
        self, data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract skill proficiencies from various data sources."""
        skills = []

        # Extract from skills data
        for item in data:
            if item.get("type") == "skill" or "ability_score" in item:
                skills.append({"name": item.get("name", ""), "type": "skill"})

        # Add standard D&D skills if not present
        standard_skills = [
            "Acrobatics",
            "Animal Handling",
            "Arcana",
            "Athletics",
            "Deception",
            "History",
            "Insight",
            "Intimidation",
            "Investigation",
            "Medicine",
            "Nature",
            "Perception",
            "Performance",
            "Persuasion",
            "Religion",
            "Sleight of Hand",
            "Stealth",
            "Survival",
        ]

        existing_names = {skill.get("name", "").lower() for skill in skills}

        for skill_name in standard_skills:
            if skill_name.lower() not in existing_names:
                skills.append({"name": skill_name, "type": "skill"})

        return skills

    def import_all_data(self):
        """Import all available scraped data."""
        total_imported = 0

        # Import proficiencies from skills
        skills_data = self.load_json_data("combined_skills")
        if skills_data:
            skill_proficiencies = self.extract_skills_from_data(skills_data)
            total_imported += self.import_proficiencies(skill_proficiencies)

        # Import equipment
        equipment_data = self.load_json_data("combined_equipment")
        if equipment_data:
            total_imported += self.import_equipment(equipment_data)

            # Extract weapon and armor proficiencies from equipment
            weapon_armor_profs = []
            for item in equipment_data:
                item_type = item.get("type", "").lower()
                if "weapon" in item_type:
                    weapon_armor_profs.append(
                        {
                            "name": f"{item.get('name', '')} Proficiency",
                            "type": "weapon",
                        }
                    )
                elif "armor" in item_type:
                    weapon_armor_profs.append(
                        {"name": f"{item.get('name', '')} Proficiency", "type": "armor"}
                    )

            if weapon_armor_profs:
                total_imported += self.import_proficiencies(weapon_armor_profs)

        # Import class features from classes data
        classes_data = self.load_json_data("combined_classes")
        if classes_data:
            class_features = []
            for cls_data in classes_data:
                # Extract features from class data
                if "raw_data" in cls_data:
                    raw = cls_data["raw_data"]
                    # Add class features if available in the raw data
                    # This would need to be expanded based on the actual API
                    # structure

                class_features.append(
                    {
                        "name": f"{cls_data.get('name', '')} Features",
                        "description": f"Core features of the {cls_data.get('name', '')} class",
                        "source": "Class",
                    }
                )

            if class_features:
                total_imported += self.import_features(class_features)

        # Import racial features from races data
        races_data = self.load_json_data("combined_races")
        if races_data:
            racial_features = []
            for race_data in races_data:
                for trait in race_data.get("traits", []):
                    racial_features.append(
                        {
                            "name": trait,
                            "description": f"Racial trait of {race_data.get('name', '')}",
                            "source": "Race",
                        }
                    )

            if racial_features:
                total_imported += self.import_features(racial_features)

        return total_imported


def main():
    """Main entry point for data import."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    importer = DataImporter()

    try:
        print("Starting data import...")
        total = importer.import_all_data()
        print(f"Import completed! Total items imported: {total}")

    except KeyboardInterrupt:
        print("\nImport interrupted by user")
    except Exception as e:
        print(f"Import failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
