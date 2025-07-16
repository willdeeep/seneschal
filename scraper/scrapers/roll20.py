"""Scraper for Roll20 D&D 5e Compendium data."""

import asyncio
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, DataProcessor


class Roll20Scraper(BaseScraper):
    """Scraper for Roll20 D&D 5e Compendium."""
    
    def __init__(self):
        super().__init__("roll20")
        self.base_url = "https://roll20.net/compendium/dnd5e"
        self.processor = DataProcessor()
    
    async def fetch_html(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch HTML content and return BeautifulSoup object."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
        
        try:
            self.logger.info("Fetching HTML from: %s", url)
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    self.logger.debug("Successfully parsed HTML from: %s", url)
                    return soup
                else:
                    self.logger.warning("HTTP %d for %s", response.status, url)
                    return None
        except Exception as e:
            self.logger.error("Error fetching HTML from %s: %s", url, e)
            return None
    
    async def scrape_proficiencies(self) -> List[Dict[str, Any]]:
        """Scrape proficiencies from Roll20 compendium."""
        url = f"{self.base_url}/Index:Proficiencies"
        soup = await self.fetch_html(url)
        
        if not soup:
            self.logger.error("Failed to fetch proficiencies page")
            return []
        
        proficiencies = []
        
        # Look for proficiency sections
        # Roll20 typically organizes proficiencies in sections like Skills, Tools, etc.
        content_div = soup.find('div', {'id': 'pagecontent'}) or soup.find('div', class_='content')
        
        if not content_div:
            self.logger.warning("Could not find content div on proficiencies page")
            return []
        
        # Find all links that look like proficiencies
        proficiency_links = content_div.find_all('a', href=re.compile(r'/compendium/dnd5e/'))
        
        for link in proficiency_links:
            prof_name = link.get_text(strip=True)
            prof_url = link.get('href')
            
            if not prof_name or not prof_url:
                continue
            
            # Skip certain types of links
            if any(skip in prof_url.lower() for skip in ['spells', 'monsters', 'items', 'classes', 'races']):
                continue
            
            # Determine proficiency type based on the link or text
            prof_type = self._determine_proficiency_type(prof_name, prof_url)
            
            proficiency = {
                'name': self.processor.normalize_name(prof_name),
                'type': prof_type,
                'source': 'Roll20 Compendium',
                'url': f"https://roll20.net{prof_url}" if prof_url.startswith('/') else prof_url
            }
            
            proficiencies.append(proficiency)
        
        # Also scrape detailed proficiency sections
        await self._scrape_proficiency_sections(soup, proficiencies)
        
        self.logger.info("Scraped %d proficiencies from Roll20", len(proficiencies))
        return proficiencies
    
    async def _scrape_proficiency_sections(self, soup: BeautifulSoup, proficiencies: List[Dict[str, Any]]):
        """Scrape organized proficiency sections from the page."""
        # Look for section headers
        headers = soup.find_all(['h2', 'h3', 'h4'])
        
        for header in headers:
            section_title = header.get_text(strip=True).lower()
            
            # Identify section type
            section_type = None
            if 'skill' in section_title:
                section_type = 'skill'
            elif 'tool' in section_title or 'kit' in section_title:
                section_type = 'tool'
            elif 'weapon' in section_title:
                section_type = 'weapon'
            elif 'armor' in section_title or 'armour' in section_title:
                section_type = 'armor'
            elif 'language' in section_title:
                section_type = 'language'
            
            if not section_type:
                continue
            
            # Find the content after this header
            current_element = header.next_sibling
            while current_element:
                if current_element.name in ['h1', 'h2', 'h3', 'h4']:
                    break
                
                if hasattr(current_element, 'find_all'):
                    # Look for lists or tables of proficiencies
                    items = current_element.find_all(['li', 'td', 'a'])
                    
                    for item in items:
                        item_text = item.get_text(strip=True)
                        if item_text and len(item_text) > 2:
                            proficiency = {
                                'name': self.processor.normalize_name(item_text),
                                'type': section_type,
                                'source': 'Roll20 Compendium',
                                'section': section_title
                            }
                            
                            # Avoid duplicates
                            if not any(p['name'] == proficiency['name'] for p in proficiencies):
                                proficiencies.append(proficiency)
                
                current_element = current_element.next_sibling
    
    def _determine_proficiency_type(self, name: str, url: str) -> str:
        """Determine the type of proficiency based on name and URL."""
        name_lower = name.lower()
        url_lower = url.lower()
        
        # Check URL patterns
        if 'skill' in url_lower:
            return 'skill'
        elif 'tool' in url_lower or 'kit' in url_lower:
            return 'tool'
        elif 'weapon' in url_lower:
            return 'weapon'
        elif 'armor' in url_lower or 'armour' in url_lower:
            return 'armor'
        elif 'language' in url_lower:
            return 'language'
        
        # Check name patterns
        if any(skill in name_lower for skill in [
            'acrobatics', 'animal handling', 'arcana', 'athletics', 'deception',
            'history', 'insight', 'intimidation', 'investigation', 'medicine',
            'nature', 'perception', 'performance', 'persuasion', 'religion',
            'sleight of hand', 'stealth', 'survival'
        ]):
            return 'skill'
        
        if any(tool in name_lower for tool in [
            'kit', 'tools', 'supplies', 'instrument', 'gaming set', 'vehicle'
        ]):
            return 'tool'
        
        if any(weapon in name_lower for weapon in [
            'sword', 'bow', 'crossbow', 'weapon', 'martial', 'simple'
        ]):
            return 'weapon'
        
        if any(armor in name_lower for armor in [
            'armor', 'armour', 'shield', 'light armor', 'medium armor', 'heavy armor'
        ]):
            return 'armor'
        
        # Default
        return 'proficiency'
    
    async def scrape_spells(self) -> List[Dict[str, Any]]:
        """Scrape spells from Roll20 compendium."""
        url = f"{self.base_url}/Spells%20List#content"
        soup = await self.fetch_html(url)
        
        if not soup:
            self.logger.error("Failed to fetch spells page")
            return []
        
        spells = []
        
        # Find the spells table or list
        content_div = soup.find('div', {'id': 'pagecontent'}) or soup.find('div', class_='content')
        
        if not content_div:
            self.logger.warning("Could not find content div on spells page")
            return []
        
        # Look for spell links
        spell_links = content_div.find_all('a', href=re.compile(r'/compendium/dnd5e/.*[Ss]pell'))
        
        if not spell_links:
            # Try alternative patterns
            spell_links = content_div.find_all('a', href=re.compile(r'/compendium/dnd5e/'))
            # Filter to only spell-looking links
            spell_links = [link for link in spell_links if self._looks_like_spell(link)]
        
        self.logger.info("Found %d potential spell links", len(spell_links))
        
        # Process spell links in batches to avoid overwhelming the server
        batch_size = 10
        for i in range(0, len(spell_links), batch_size):
            batch = spell_links[i:i + batch_size]
            
            tasks = []
            for link in batch:
                spell_url = link.get('href')
                if spell_url and spell_url.startswith('/'):
                    full_url = f"https://roll20.net{spell_url}"
                    tasks.append(self._scrape_spell_details(full_url, link.get_text(strip=True)))
            
            # Execute batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, dict):
                    spells.append(result)
            
            # Be nice to the server
            await asyncio.sleep(1)
        
        self.logger.info("Scraped %d spells from Roll20", len(spells))
        return spells
    
    def _looks_like_spell(self, link) -> bool:
        """Check if a link looks like it points to a spell."""
        text = link.get_text(strip=True).lower()
        href = link.get('href', '').lower()
        
        # Skip obviously non-spell links
        if any(skip in href for skip in ['class', 'race', 'equipment', 'monster', 'feat']):
            return False
        
        # Spell names often contain certain patterns
        if any(pattern in text for pattern in ['spell', 'cantrip', 'ritual']):
            return True
        
        # Check if it looks like a spell name (capitalized, not too long)
        if len(text) > 50 or len(text) < 3:
            return False
        
        # Spells often have specific word patterns
        spell_indicators = [
            'acid', 'fire', 'ice', 'lightning', 'magic', 'arcane', 'divine',
            'heal', 'cure', 'bless', 'curse', 'summon', 'create', 'detect',
            'shield', 'ward', 'protection', 'illusion', 'charm', 'hold',
            'light', 'darkness', 'bolt', 'ray', 'missile', 'arrow'
        ]
        
        if any(indicator in text for indicator in spell_indicators):
            return True
        
        # If the link has spell-like URL structure
        if 'spell' in href or text.replace(' ', '').isalpha():
            return True
        
        return False
    
    async def _scrape_spell_details(self, url: str, spell_name: str) -> Optional[Dict[str, Any]]:
        """Scrape detailed spell information from a spell page."""
        soup = await self.fetch_html(url)
        
        if not soup:
            return None
        
        try:
            spell_data = {
                'name': self.processor.normalize_name(spell_name),
                'source': 'Roll20 Compendium',
                'url': url
            }
            
            # Find the spell details section
            content_div = soup.find('div', {'id': 'pagecontent'}) or soup.find('div', class_='content')
            
            if not content_div:
                return spell_data
            
            # Extract spell level
            level_text = content_div.get_text()
            level_match = re.search(r'(\d+)(?:st|nd|rd|th)[\s-]*level', level_text, re.IGNORECASE)
            if level_match:
                spell_data['level'] = int(level_match.group(1))
            elif 'cantrip' in level_text.lower():
                spell_data['level'] = 0
            
            # Extract school
            school_match = re.search(r'\b(abjuration|conjuration|divination|enchantment|evocation|illusion|necromancy|transmutation)\b', level_text, re.IGNORECASE)
            if school_match:
                spell_data['school'] = school_match.group(1).capitalize()
            
            # Extract casting time
            casting_match = re.search(r'casting time:?\s*([^.\n]+)', level_text, re.IGNORECASE)
            if casting_match:
                spell_data['casting_time'] = casting_match.group(1).strip()
            
            # Extract range
            range_match = re.search(r'range:?\s*([^.\n]+)', level_text, re.IGNORECASE)
            if range_match:
                spell_data['range'] = range_match.group(1).strip()
            
            # Extract components
            components_match = re.search(r'components:?\s*([^.\n]+)', level_text, re.IGNORECASE)
            if components_match:
                components_text = components_match.group(1).strip()
                spell_data['components'] = [c.strip() for c in components_text.split(',')]
            
            # Extract duration
            duration_match = re.search(r'duration:?\s*([^.\n]+)', level_text, re.IGNORECASE)
            if duration_match:
                spell_data['duration'] = duration_match.group(1).strip()
                spell_data['concentration'] = 'concentration' in spell_data['duration'].lower()
            
            # Extract description
            description_paragraphs = content_div.find_all('p')
            description_parts = []
            for p in description_paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 20:  # Filter out short non-description text
                    description_parts.append(text)
            
            if description_parts:
                spell_data['description'] = self.processor.clean_text(' '.join(description_parts))
            
            # Check for ritual
            spell_data['ritual'] = 'ritual' in level_text.lower()
            
            return spell_data
            
        except Exception as e:
            self.logger.warning("Error extracting spell details for %s: %s", spell_name, e)
            return spell_data
    
    async def scrape(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape all configured data types from Roll20."""
        results = {}
        
        self.logger.info("Starting Roll20 scraping...")
        
        # Scrape proficiencies
        self.logger.info("Scraping proficiencies...")
        results['proficiencies'] = await self.scrape_proficiencies()
        
        # Scrape spells
        self.logger.info("Scraping spells...")
        results['spells'] = await self.scrape_spells()
        
        self.logger.info("Roll20 scraping completed")
        return results
