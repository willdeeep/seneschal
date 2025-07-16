"""Main scraper orchestrator for D&D data collection."""

import asyncio
import logging
import os
import sys
from typing import Dict, List, Any

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SCRAPE_CONFIG, LOG_LEVEL, LOG_FILE, DATA_DIR
from scrapers.base import setup_data_directories
from scrapers.dnd5e_api import DnD5eAPIScraper
from scrapers.roll20 import Roll20Scraper


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


class ScraperOrchestrator:
    """Orchestrates multiple scrapers to collect D&D data."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scrapers = []
        self.results = {}
        
        # Initialize scrapers based on configuration
        if SCRAPE_CONFIG.get('races') or SCRAPE_CONFIG.get('classes') or \
           SCRAPE_CONFIG.get('equipment') or SCRAPE_CONFIG.get('spells') or \
           SCRAPE_CONFIG.get('skills'):
            self.scrapers.append(DnD5eAPIScraper())
            
        # Add Roll20 scraper for additional proficiencies and spells
        if SCRAPE_CONFIG.get('skills') or SCRAPE_CONFIG.get('spells'):
            self.scrapers.append(Roll20Scraper())
    
    async def run_scraping(self) -> Dict[str, Any]:
        """Run all configured scrapers."""
        self.logger.info("Starting data scraping process...")
        
        # Set up data directories
        setup_data_directories()
        
        all_results = {}
        
        # Run each scraper
        for scraper in self.scrapers:
            try:
                self.logger.info("Running scraper: %s", scraper.name)
                async with scraper:
                    scraper_results = await scraper.scrape()
                    
                    # Merge results
                    for data_type, items in scraper_results.items():
                        if data_type not in all_results:
                            all_results[data_type] = []
                        all_results[data_type].extend(items)
                        
                        # Save individual data type
                        scraper.save_data(items, f"{data_type}_{scraper.name}")
                        
                self.logger.info("Completed scraper: %s", scraper.name)
                
            except Exception as e:
                self.logger.error("Error running scraper %s: %s", scraper.name, e)
                continue
        
        # Save combined results
        self._save_combined_results(all_results)
        
        # Print summary
        self._print_summary(all_results)
        
        return all_results
    
    def _save_combined_results(self, results: Dict[str, List[Any]]):
        """Save combined results from all scrapers."""
        for data_type, items in results.items():
            if items:
                filename = f"combined_{data_type}"
                filepath = os.path.join(DATA_DIR, f"{filename}.json")
                
                try:
                    import json
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(items, f, indent=2, ensure_ascii=False)
                    self.logger.info("Saved %d combined %s items to %s", len(items), data_type, filepath)
                except Exception as e:
                    self.logger.error("Failed to save combined %s data: %s", data_type, e)
    
    def _print_summary(self, results: Dict[str, List[Any]]):
        """Print a summary of scraped data."""
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        
        total_items = 0
        for data_type, items in results.items():
            count = len(items)
            total_items += count
            print(f"{data_type.capitalize()}: {count} items")
        
        print(f"\nTotal items scraped: {total_items}")
        print(f"Data saved to: {DATA_DIR}")
        print("="*50)


async def main():
    """Main entry point for the scraper."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        orchestrator = ScraperOrchestrator()
        results = await orchestrator.run_scraping()
        
        logger.info("Scraping completed successfully")
        return results
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        return None
    except Exception as e:
        logger.error("Scraping failed: %s", e)
        return None


if __name__ == "__main__":
    # Run the scraper
    results = asyncio.run(main())
    
    if results:
        print("\nScraping completed successfully!")
        print("To import this data into your database, run:")
        print("python import_data.py")
    else:
        print("\nScraping failed or was interrupted.")
        sys.exit(1)
