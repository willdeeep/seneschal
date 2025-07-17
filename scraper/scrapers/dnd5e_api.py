"""Scraper for D&D 5e API data."""

import asyncio
from typing import Dict, List, Any
from scrapers.base import BaseScraper, DataProcessor
from config import DND5E_API_BASE_URL


class DnD5eAPIScraper(BaseScraper):
    """Scraper for the D&D 5e API (dnd5eapi.co)."""

    def __init__(self):
        super().__init__("dnd5e_api")
        self.base_url = DND5E_API_BASE_URL
        self.processor = DataProcessor()

    async def scrape_endpoint(self, endpoint: str) -> List[Dict[str, Any]]:
        """Scrape a specific endpoint and return detailed items."""
        # Get the list of items
        list_url = f"{self.base_url}/{endpoint}"
        list_data = await self.fetch_json(list_url)

        if not list_data or "results" not in list_data:
            self.logger.warning("No results found for endpoint: %s", endpoint)
            return []

        items = []
        total_items = len(list_data["results"])

        self.logger.info("Scraping %d items from %s", total_items, endpoint)

        # Fetch detailed data for each item
        tasks = []
        for item in list_data["results"]:
            if "url" in item:
                # Fix the URL structure - remove duplicate path parts
                detail_url = item["url"]
                if detail_url.startswith("/api/"):
                    detail_url = f"{self.base_url}{detail_url}"
                else:
                    detail_url = f"{self.base_url}/{detail_url}"
                tasks.append(self.fetch_json(detail_url))

        # Execute all requests
        detailed_items = await asyncio.gather(*tasks, return_exceptions=True)

        for i, detail in enumerate(detailed_items):
            if isinstance(detail, dict):
                items.append(detail)
            else:
                self.logger.warning(
                    "Failed to fetch details for item %d: %s", i, detail
                )

        self.logger.info(
            "Successfully scraped %d/%d items from %s",
            len(items),
            total_items,
            endpoint,
        )
        return items

    async def scrape_races(self) -> List[Dict[str, Any]]:
        """Scrape race data."""
        races = await self.scrape_endpoint("races")
        processed_races = []

        for race in races:
            processed_race = {
                "name": self.processor.normalize_name(race.get("name", "")),
                "size": race.get("size", ""),
                "speed": race.get("speed", {}).get("walk", 30),
                "languages": [
                    lang.get("name", "") for lang in race.get("languages", [])
                ],
                "proficiencies": [
                    prof.get("name", "") for prof in race.get("proficiencies", [])
                ],
                "traits": [trait.get("name", "") for trait in race.get("traits", [])],
                "ability_bonuses": race.get("ability_bonuses", []),
                "subraces": [
                    subrace.get("name", "") for subrace in race.get("subraces", [])
                ],
                "source": "D&D 5e API",
                "raw_data": race,
            }
            processed_races.append(processed_race)

        return processed_races

    async def scrape_classes(self) -> List[Dict[str, Any]]:
        """Scrape class data."""
        classes = await self.scrape_endpoint("classes")
        processed_classes = []

        for cls in classes:
            processed_class = {
                "name": self.processor.normalize_name(cls.get("name", "")),
                "hit_die": cls.get("hit_die", 8),
                "primary_abilities": [
                    ability.get("name", "")
                    for ability in cls.get("primary_ability", [])
                ],
                "saving_throw_proficiencies": [
                    save.get("name", "") for save in cls.get("saving_throws", [])
                ],
                "skill_proficiencies": [
                    skill.get("name", "")
                    for skill in cls.get("proficiencies", [])
                    if "Skill:" in skill.get("name", "")
                ],
                "equipment_proficiencies": [
                    prof.get("name", "")
                    for prof in cls.get("proficiencies", [])
                    if "Skill:" not in prof.get("name", "")
                ],
                "starting_equipment": cls.get("starting_equipment", []),
                "spellcasting": cls.get("spellcasting", {}),
                "subclasses": [
                    sub.get("name", "") for sub in cls.get("subclasses", [])
                ],
                "source": "D&D 5e API",
                "raw_data": cls,
            }
            processed_classes.append(processed_class)

        return processed_classes

    async def scrape_equipment(self) -> List[Dict[str, Any]]:
        """Scrape equipment data."""
        equipment = await self.scrape_endpoint("equipment")
        processed_equipment = []

        for item in equipment:
            processed_item = {
                "name": self.processor.normalize_name(item.get("name", "")),
                "type": item.get("equipment_category", {}).get("name", "").lower(),
                "cost": self._parse_cost(item.get("cost", {})),
                "weight": item.get("weight", 0),
                "description": self.processor.clean_text(
                    item.get("desc", [""])[0] if item.get("desc") else ""
                ),
                "properties": [
                    prop.get("name", "") for prop in item.get("properties", [])
                ],
                "source": "D&D 5e API",
                "raw_data": item,
            }

            # Add weapon-specific data
            if "weapon" in processed_item["type"].lower():
                damage = item.get("damage", {})
                processed_item.update(
                    {
                        "damage_dice": damage.get("damage_dice", ""),
                        "damage_type": damage.get("damage_type", {}).get("name", ""),
                        "weapon_category": item.get("weapon_category", ""),
                        "weapon_range": item.get("weapon_range", ""),
                        "range_normal": item.get("range", {}).get("normal", 0),
                        "range_long": item.get("range", {}).get("long", 0),
                    }
                )

            # Add armor-specific data
            elif "armor" in processed_item["type"].lower():
                armor_class = item.get("armor_class", {})
                processed_item.update(
                    {
                        "armor_class_base": armor_class.get("base", 10),
                        "armor_class_dex_bonus": armor_class.get("dex_bonus", True),
                        "armor_class_max_bonus": armor_class.get("max_bonus", None),
                        "armor_category": item.get("armor_category", ""),
                        "stealth_disadvantage": item.get("stealth_disadvantage", False),
                        "strength_requirement": item.get("str_minimum", 0),
                    }
                )

            processed_equipment.append(processed_item)

        return processed_equipment

    async def scrape_spells(self) -> List[Dict[str, Any]]:
        """Scrape spell data."""
        spells = await self.scrape_endpoint("spells")
        processed_spells = []

        for spell in spells:
            processed_spell = {
                "name": self.processor.normalize_name(spell.get("name", "")),
                "level": spell.get("level", 0),
                "school": spell.get("school", {}).get("name", ""),
                "casting_time": spell.get("casting_time", ""),
                "range": spell.get("range", ""),
                "components": spell.get("components", []),
                "duration": spell.get("duration", ""),
                "concentration": spell.get("concentration", False),
                "ritual": spell.get("ritual", False),
                "description": self.processor.clean_text(
                    "\n".join(spell.get("desc", []))
                ),
                "higher_level": self.processor.clean_text(
                    "\n".join(spell.get("higher_level", []))
                ),
                "classes": [cls.get("name", "") for cls in spell.get("classes", [])],
                "damage": spell.get("damage", {}),
                "heal_at_slot_level": spell.get("heal_at_slot_level", {}),
                "source": "D&D 5e API",
                "raw_data": spell,
            }
            processed_spells.append(processed_spell)

        return processed_spells

    async def scrape_skills(self) -> List[Dict[str, Any]]:
        """Scrape skill data."""
        skills = await self.scrape_endpoint("skills")
        processed_skills = []

        for skill in skills:
            processed_skill = {
                "name": self.processor.normalize_name(skill.get("name", "")),
                "ability_score": skill.get("ability_score", {}).get("name", ""),
                "description": self.processor.clean_text(
                    "\n".join(skill.get("desc", []))
                ),
                "type": "skill",
                "source": "D&D 5e API",
                "raw_data": skill,
            }
            processed_skills.append(processed_skill)

        return processed_skills

    def _parse_cost(self, cost_data: Dict[str, Any]) -> int:
        """Parse cost data and return value in copper pieces."""
        if not cost_data:
            return 0

        quantity = cost_data.get("quantity", 0)
        unit = cost_data.get("unit", "cp").lower()

        # Convert to copper pieces
        multipliers = {"cp": 1, "sp": 10, "ep": 50, "gp": 100, "pp": 1000}

        return quantity * multipliers.get(unit, 1)

    async def scrape(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape all configured data types."""
        results = {}

        # Scrape each data type
        self.logger.info("Starting D&D 5e API scraping...")

        results["races"] = await self.scrape_races()
        results["classes"] = await self.scrape_classes()
        results["equipment"] = await self.scrape_equipment()
        results["spells"] = await self.scrape_spells()
        results["skills"] = await self.scrape_skills()

        self.logger.info("D&D 5e API scraping completed")
        return results
