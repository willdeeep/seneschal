"""
D20 SRD scraper for comprehensive D&D 5e data collection.
"""

from scrapers.base import BaseScraper
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import sys

# Add the parent directory to the path so we can import base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class D20SRDScraper(BaseScraper):
    """Scraper for D20 SRD website - much more reliable than Roll20."""

    def __init__(self):
        super().__init__("d20srd")
        self.base_url = "https://5e.d20srd.org"
        self.skills_data = {}

    async def fetch_page(self, session, url):
        """Fetch a page with proper error handling."""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    self.logger.warning(f"Failed to fetch {url}: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error fetching {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching {url}: {e}")
            return None

    async def scrape_skills(self):
        """Scrape all skills and their associated abilities from D20 SRD."""
        skills_url = f"{self.base_url}/srd/skills/usingEachAbility.htm"

        self.logger.info(f"Scraping skills from: {skills_url}")

        async with aiohttp.ClientSession() as session:
            try:
                html_content = await self.fetch_page(session, skills_url)
                if not html_content:
                    self.logger.error("Failed to fetch skills page")
                    return {}

                soup = BeautifulSoup(html_content, "html.parser")
                skills = self._parse_skills_from_abilities_page(soup)

                self.logger.info(f"Found {len(skills)} skills")
                return skills

            except aiohttp.ClientError as e:
                self.logger.error(f"Network error scraping skills: {e}")
                return {}
            except Exception as e:
                self.logger.error(f"Unexpected error scraping skills: {e}")
                return {}

    def _parse_skills_from_abilities_page(self, soup):
        """Parse skills organized by ability from the abilities page."""
        skills = {}

        # Define the ability-to-skill mapping based on D&D 5e rules
        ability_skills = {
            "strength": ["Athletics"],
            "dexterity": ["Acrobatics", "Sleight of Hand", "Stealth"],
            "constitution": [],  # No skills use Constitution
            "intelligence": [
                "Arcana",
                "History",
                "Investigation",
                "Nature",
                "Religion",
            ],
            "wisdom": [
                "Animal Handling",
                "Insight",
                "Medicine",
                "Perception",
                "Survival",
            ],
            "charisma": ["Deception", "Intimidation", "Performance", "Persuasion"],
        }

        # Extract detailed descriptions for each skill
        for ability, skill_list in ability_skills.items():
            for skill_name in skill_list:
                # Try to find the skill section in the HTML
                skill_description = self._extract_skill_description(
                    soup, skill_name, ability
                )

                skills[skill_name] = {
                    "name": skill_name,
                    "ability": ability,
                    "description": skill_description,
                    "type": "skill",
                }

        return skills

    def _extract_skill_description(self, soup, skill_name, ability):
        """Extract description for a specific skill."""
        # Look for the skill heading and extract following content
        skill_id = skill_name.lower().replace(" ", "").replace("'", "")

        # Try multiple approaches to find the skill description
        skill_element = soup.find("a", {"name": skill_id}) or soup.find(id=skill_id)

        if skill_element:
            # Find the next paragraph or div containing description
            description_element = skill_element.find_next("p")
            if description_element:
                return description_element.get_text(strip=True)

        # Fallback descriptions if we can't scrape them
        fallback_descriptions = {
            "Athletics": "Your Strength (Athletics) check covers difficult situations you encounter while climbing, jumping, or swimming.",
            "Acrobatics": "Your Dexterity (Acrobatics) check covers your attempt to stay on your feet in a tricky situation.",
            "Sleight of Hand": "Whenever you attempt an act of legerdemain or manual trickery, make a Dexterity (Sleight of Hand) check.",
            "Stealth": "Make a Dexterity (Stealth) check when you attempt to conceal yourself from enemies.",
            "Arcana": "Your Intelligence (Arcana) check measures your ability to recall lore about spells, magic items, eldritch symbols, magical traditions, and the planes of existence.",
            "History": "Your Intelligence (History) check measures your ability to recall lore about historical events, legendary people, ancient kingdoms, past disputes, recent wars, and lost civilizations.",
            "Investigation": "When you look around for clues and make deductions based on those clues, you make an Intelligence (Investigation) check.",
            "Nature": "Your Intelligence (Nature) check measures your ability to recall lore about terrain, plants and animals, the weather, and natural cycles.",
            "Religion": "Your Intelligence (Religion) check measures your ability to recall lore about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults.",
            "Animal Handling": "When there is any question whether you can calm down a domesticated animal, keep a mount from getting spooked, or intuit an animal's intentions, make a Wisdom (Animal Handling) check.",
            "Insight": "Your Wisdom (Insight) check decides whether you can determine the true intentions of a creature.",
            "Medicine": "A Wisdom (Medicine) check lets you try to stabilize a dying companion or diagnose an illness.",
            "Perception": "Your Wisdom (Perception) check lets you spot, hear, or otherwise detect the presence of something.",
            "Survival": "Your Wisdom (Survival) check to follow tracks, hunt wild game, guide your group through frozen wastelands, identify signs that owlbears live nearby, predict the weather, or avoid quicksand and other natural hazards.",
            "Deception": "Your Charisma (Deception) check determines whether you can convincingly hide the truth, either verbally or through your actions.",
            "Intimidation": "When you attempt to influence someone through overt threats, hostile actions, and physical violence, make a Charisma (Intimidation) check.",
            "Performance": "Your Charisma (Performance) check determines how well you can delight an audience with music, dance, acting, storytelling, or some other form of entertainment.",
            "Persuasion": "When you attempt to influence someone or a group of people with tact, social graces, or good nature, make a Charisma (Persuasion) check.",
        }

        return fallback_descriptions.get(skill_name, f"A {ability} based skill check.")

    async def scrape_equipment(self):
        """Scrape equipment data from D20 SRD."""
        equipment_url = f"{self.base_url}/indexes/equipment.htm"

        self.logger.info(f"Scraping equipment from: {equipment_url}")

        async with aiohttp.ClientSession() as session:
            try:
                html_content = await self.fetch_page(session, equipment_url)
                if not html_content:
                    self.logger.error("Failed to fetch equipment page")
                    return {}

                soup = BeautifulSoup(html_content, "html.parser")
                equipment = self._parse_equipment_page(soup)

                self.logger.info(f"Found {len(equipment)} equipment items")
                return equipment

            except aiohttp.ClientError as e:
                self.logger.error(f"Network error scraping equipment: {e}")
                return {}
            except Exception as e:
                self.logger.error(f"Unexpected error scraping equipment: {e}")
                return {}

    def _parse_equipment_page(self, soup):
        """Parse equipment from the equipment index page."""
        equipment = {}

        # Look for links to equipment pages
        equipment_links = soup.find_all("a", href=True)

        for link in equipment_links:
            href = link.get("href", "")
            text = link.get_text(strip=True)

            # Filter for equipment-related links
            if (
                "equipment" in href.lower()
                or "armor" in href.lower()
                or "weapons" in href.lower()
            ) and text:

                equipment[text] = {
                    "name": text,
                    "url": (
                        f"{self.base_url}/{href}"
                        if not href.startswith("http")
                        else href
                    ),
                    "type": self._categorize_equipment(text, href),
                }

        return equipment

    def _categorize_equipment(self, name, href):
        """Categorize equipment based on name and URL."""
        name_lower = name.lower()

        if any(
            weapon in name_lower
            for weapon in ["sword", "axe", "bow", "dagger", "spear", "mace", "hammer"]
        ):
            return "weapon"
        elif any(
            armor in name_lower
            for armor in ["armor", "mail", "plate", "leather", "shield"]
        ):
            return "armor"
        elif "tool" in name_lower or "kit" in name_lower:
            return "tool"
        elif any(
            consumable in name_lower
            for consumable in ["potion", "scroll", "ration", "oil"]
        ):
            return "consumable"
        else:
            return "gear"

    async def scrape_spells(self):
        """Scrape spell data from D20 SRD."""
        spells_url = f"{self.base_url}/indexes/spells.htm"

        self.logger.info(f"Scraping spells from: {spells_url}")

        async with aiohttp.ClientSession() as session:
            try:
                html_content = await self.fetch_page(session, spells_url)
                if not html_content:
                    self.logger.error("Failed to fetch spells page")
                    return {}

                soup = BeautifulSoup(html_content, "html.parser")
                spells = self._parse_spells_page(soup)

                self.logger.info(f"Found {len(spells)} spells")
                return spells

            except aiohttp.ClientError as e:
                self.logger.error(f"Network error scraping spells: {e}")
                return {}
            except Exception as e:
                self.logger.error(f"Unexpected error scraping spells: {e}")
                return {}

    def _parse_spells_page(self, soup):
        """Parse spells from the spells index page."""
        spells = {}

        # Look for spell links
        spell_links = soup.find_all("a", href=True)

        for link in spell_links:
            href = link.get("href", "")
            text = link.get_text(strip=True)

            # Filter for spell-related links
            if "spells" in href.lower() and text and len(text) > 2:
                spells[text] = {
                    "name": text,
                    "url": (
                        f"{self.base_url}/{href}"
                        if not href.startswith("http")
                        else href
                    ),
                    "school": self._guess_spell_school(text),
                    "level": self._guess_spell_level(text),
                }

        return spells

    def _guess_spell_school(self, spell_name):
        """Make an educated guess about spell school based on name."""
        school_keywords = {
            "evocation": [
                "fire",
                "lightning",
                "force",
                "magic missile",
                "fireball",
                "eldritch blast",
            ],
            "illusion": ["illusion", "invisible", "disguise", "mirror", "phantom"],
            "enchantment": ["charm", "command", "suggestion", "dominate", "compulsion"],
            "necromancy": ["death", "undead", "vampire", "animate", "speak with dead"],
            "transmutation": ["transform", "polymorph", "enhance", "alter", "enlarge"],
            "conjuration": ["summon", "create", "conjure", "teleport", "dimension"],
            "abjuration": ["protect", "shield", "ward", "dispel", "counterspell"],
            "divination": ["detect", "identify", "locate", "scry", "foresight"],
        }

        spell_lower = spell_name.lower()
        for school, keywords in school_keywords.items():
            if any(keyword in spell_lower for keyword in keywords):
                return school

        return "unknown"

    def _guess_spell_level(self, spell_name):
        """Attempt to guess spell level from name (basic heuristic)."""
        # This is very basic - in reality we'd need to scrape individual spell
        # pages
        if any(
            cantrip in spell_name.lower()
            for cantrip in ["light", "mage hand", "prestidigitation"]
        ):
            return 0
        return 1  # Default to 1st level

    async def scrape(self):
        """Implementation of the abstract scrape method from BaseScraper."""
        return await self.scrape_all_data()

    async def scrape_all_data(self):
        """Scrape all D&D data from D20 SRD."""
        self.logger.info("Starting comprehensive D20 SRD scraping...")

        # Scrape all data types concurrently
        skills_task = self.scrape_skills()
        equipment_task = self.scrape_equipment()
        spells_task = self.scrape_spells()

        skills, equipment, spells = await asyncio.gather(
            skills_task, equipment_task, spells_task
        )

        return {"skills": skills, "equipment": equipment, "spells": spells}


async def main():
    """Main function to test the D20 SRD scraper."""
    scraper = D20SRDScraper()

    # Test skills scraping
    skills = await scraper.scrape_skills()
    print(f"\nSkills found: {len(skills)}")
    for skill_name, skill_data in list(skills.items())[:3]:
        print(
            f"- {skill_name} ({skill_data['ability']}): {skill_data['description'][:100]}..."
        )

    # Test equipment scraping
    equipment = await scraper.scrape_equipment()
    print(f"\nEquipment found: {len(equipment)}")
    for item_name, item_data in list(equipment.items())[:3]:
        print(f"- {item_name} ({item_data['type']})")

    # Test spells scraping
    spells = await scraper.scrape_spells()
    print(f"\nSpells found: {len(spells)}")
    for spell_name, spell_data in list(spells.items())[:3]:
        print(f"- {spell_name} ({spell_data['school']}, level {spell_data['level']})")


if __name__ == "__main__":
    asyncio.run(main())
