"""Simple test script to verify the scraper functionality."""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.dnd5e_api import DnD5eAPIScraper


async def test_scraper():
    """Test the D&D 5e API scraper with a small subset of data."""
    print("Testing D&D 5e API Scraper...")
    print("=" * 40)

    try:
        async with DnD5eAPIScraper() as scraper:
            # Test fetching a single endpoint
            print("Testing basic API connectivity...")
            
            # Test races endpoint
            races_url = f"{scraper.base_url}/races"
            races_list = await scraper.fetch_json(races_url)
            
            if races_list and 'results' in races_list:
                race_count = len(races_list['results'])
                print(f"✓ Successfully connected to API")
                print(f"✓ Found {race_count} races available")
                
                # Test detailed fetch for first race
                if race_count > 0:
                    first_race_url = f"{scraper.base_url}{races_list['results'][0]['url']}"
                    race_detail = await scraper.fetch_json(first_race_url)
                    
                    if race_detail:
                        print(f"✓ Successfully fetched detailed data for: {race_detail.get('name', 'Unknown')}")
                    else:
                        print("✗ Failed to fetch detailed race data")
                        return False
                
                # Test equipment endpoint
                print("\nTesting equipment endpoint...")
                equipment_url = f"{scraper.base_url}/equipment"
                equipment_list = await scraper.fetch_json(equipment_url)
                
                if equipment_list and 'results' in equipment_list:
                    equipment_count = len(equipment_list['results'])
                    print(f"✓ Found {equipment_count} equipment items available")
                else:
                    print("✗ Failed to fetch equipment list")
                    return False
                
                print("\n" + "=" * 40)
                print("Scraper test completed successfully!")
                print("The scraper is ready to collect D&D data.")
                return True
                
            else:
                print("✗ Failed to connect to D&D 5e API")
                return False
                
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False


def test_data_processing():
    """Test data processing utilities."""
    print("\nTesting data processing...")

    from scrapers.base import DataProcessor

    processor = DataProcessor()

    # Test text cleaning
    dirty_text = "  **This is bold text**  with   extra   spaces  "
    clean_text = processor.clean_text(dirty_text)
    expected = "This is bold text with extra spaces"

    if clean_text == expected:
        print("✓ Text cleaning works correctly")
    else:
        print(f"✗ Text cleaning failed: got '{clean_text}', expected '{expected}'")
        return False

    # Test name normalization
    messy_name = "longsword of sharpness"
    normalized_name = processor.normalize_name(messy_name)
    expected_name = "Longsword Of Sharpness"

    if normalized_name == expected_name:
        print("✓ Name normalization works correctly")
    else:
        print(f"✗ Name normalization failed: got '{normalized_name}', expected '{expected_name}'")
        return False

    # Test dice parsing
    dice_str = "2d6+3"
    dice_data = processor.parse_dice(dice_str)

    if dice_data.get('count') == 2 and dice_data.get('sides') == 6 and dice_data.get('modifier') == 3:
        print("✓ Dice parsing works correctly")
    else:
        print(f"✗ Dice parsing failed: {dice_data}")
        return False

    return True


async def main():
    """Run all tests."""
    print("D&D Data Scraper Test Suite")
    print("=" * 50)

    # Test data processing
    if not test_data_processing():
        print("\n✗ Data processing tests failed!")
        return False

    # Test scraper connectivity
    if not await test_scraper():
        print("\n✗ Scraper tests failed!")
        return False

    print("\n" + "=" * 50)
    print("✓ All tests passed! The scraper is ready to use.")
    print("\nTo run the full scraper, execute:")
    print("  python scraper.py")
    print("\nOr use the convenience script:")
    print("  bash run_scraper.sh")

    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
