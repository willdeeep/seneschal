"""Test script specifically for Roll20 scraper."""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.roll20 import Roll20Scraper


async def test_roll20_scraper():
    """Test the Roll20 scraper with the specific URLs provided."""
    print("Testing Roll20 Scraper...")
    print("=" * 40)

    try:
        async with Roll20Scraper() as scraper:
            print("✓ Scraper initialized successfully")
            
            # Test proficiencies page
            print("\nTesting proficiencies scraping...")
            proficiencies = await scraper.scrape_proficiencies()
            
            if proficiencies:
                print(f"✓ Found {len(proficiencies)} proficiencies")
                
                # Show some examples
                print("\nSample proficiencies:")
                for i, prof in enumerate(proficiencies[:5]):
                    print(f"  {i+1}. {prof['name']} ({prof['type']})")
                
                # Count by type
                type_counts = {}
                for prof in proficiencies:
                    prof_type = prof.get('type', 'unknown')
                    type_counts[prof_type] = type_counts.get(prof_type, 0) + 1
                
                print(f"\nProficiencies by type:")
                for prof_type, count in sorted(type_counts.items()):
                    print(f"  {prof_type}: {count}")
            else:
                print("✗ No proficiencies found")
                return False
            
            # Test spells page (limit to avoid overwhelming)
            print(f"\nTesting spells scraping (limited test)...")
            
            # For testing, we'll just check if we can access the page
            spells_url = f"{scraper.base_url}/Spells%20List#content"
            soup = await scraper.fetch_html(spells_url)
            
            if soup:
                print("✓ Successfully accessed spells page")
                
                # Count potential spell links
                content_div = soup.find('div', {'id': 'pagecontent'}) or soup.find('div', class_='content')
                if content_div:
                    import re
                    spell_links = content_div.find_all('a', href=re.compile(r'/compendium/dnd5e/'))
                    spell_like_links = [link for link in spell_links if scraper._looks_like_spell(link)]
                    
                    print(f"✓ Found {len(spell_like_links)} potential spell links")
                    
                    # Show some examples
                    if spell_like_links:
                        print("\nSample spell names:")
                        for i, link in enumerate(spell_like_links[:5]):
                            print(f"  {i+1}. {link.get_text(strip=True)}")
                else:
                    print("⚠ Could not find content section on spells page")
            else:
                print("✗ Failed to access spells page")
                return False
            
            print("\n" + "=" * 40)
            print("✓ Roll20 scraper test completed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False


async def main():
    """Run Roll20 scraper tests."""
    print("Roll20 D&D Data Scraper Test")
    print("=" * 50)

    success = await test_roll20_scraper()

    if success:
        print("\n✓ Roll20 scraper is working correctly!")
        print("\nTo run the full Roll20 scraper, execute:")
        print("  python scraper.py")
        print("\nOr to run with Roll20 data only:")
        print("  python -c \"")
        print("import asyncio")
        print("from scrapers.roll20 import Roll20Scraper")
        print("async def run():")
        print("    async with Roll20Scraper() as scraper:")
        print("        results = await scraper.scrape()")
        print("        scraper.save_data(results['proficiencies'], 'roll20_proficiencies')")
        print("        scraper.save_data(results['spells'], 'roll20_spells')")
        print("asyncio.run(run())")
        print("\"")
    else:
        print("\n✗ Roll20 scraper tests failed!")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
