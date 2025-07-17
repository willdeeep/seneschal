"""Debug script to examine Roll20 page structure."""

import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def examine_roll20_pages():
    """Examine the structure of Roll20 pages to understand how to scrape them."""

    urls = [
        "https://roll20.net/compendium/dnd5e/Index:Proficiencies",
        "https://roll20.net/compendium/dnd5e/Spells%20List"
    ]

    async with aiohttp.ClientSession() as session:
        for url in urls:
            print(f"\nExamining: {url}")
            print("=" * 60)
            
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"HTTP {response.status} - skipping")
                        continue
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Check page title
                    title = soup.find('title')
                    if title:
                        print(f"Page title: {title.get_text(strip=True)}")
                    
                    # Look for main content areas
                    print("\nLooking for content containers:")
                    
                    # Common content container patterns
                    containers = [
                        soup.find('div', {'id': 'pagecontent'}),
                        soup.find('div', {'id': 'content'}),
                        soup.find('div', class_='content'),
                        soup.find('div', class_='page-content'),
                        soup.find('main'),
                        soup.find('article'),
                        soup.find('div', class_='compendium-content'),
                        soup.find('div', class_='wiki-content'),
                    ]
                    
                    found_containers = [c for c in containers if c is not None]
                    print(f"Found {len(found_containers)} potential content containers")
                    
                    if found_containers:
                        main_container = found_containers[0]
                        print(f"Using container: {main_container.name} with class='{main_container.get('class')}' id='{main_container.get('id')}'")
                        
                        # Look for links
                        links = main_container.find_all('a', href=True)
                        print(f"Found {len(links)} links in main container")
                        
                        # Show some example links
                        print("\nSample links:")
                        for i, link in enumerate(links[:10]):
                            href = link.get('href')
                            text = link.get_text(strip=True)
                            print(f"  {i+1}. '{text}' -> {href}")
                        
                        # Look for tables
                        tables = main_container.find_all('table')
                        print(f"\nFound {len(tables)} tables")
                        
                        # Look for lists
                        lists = main_container.find_all(['ul', 'ol'])
                        print(f"Found {len(lists)} lists")
                        
                        if lists:
                            print("Sample list items:")
                            for i, lst in enumerate(lists[:3]):
                                items = lst.find_all('li')
                                print(f"  List {i+1}: {len(items)} items")
                                for j, item in enumerate(items[:3]):
                                    print(f"    - {item.get_text(strip=True)}")
                    
                    else:
                        print("No standard content containers found")
                        
                        # Try to find any divs with substantial content
                        all_divs = soup.find_all('div')
                        content_divs = []
                        
                        for div in all_divs:
                            text = div.get_text(strip=True)
                            if len(text) > 100:  # Substantial content
                                content_divs.append((div, len(text)))
                        
                        content_divs.sort(key=lambda x: x[1], reverse=True)
                        
                        print(f"Found {len(content_divs)} divs with substantial content")
                        if content_divs:
                            largest_div = content_divs[0][0]
                            print(f"Largest content div: class='{largest_div.get('class')}' id='{largest_div.get('id')}' ({content_divs[0][1]} chars)")
                    
                    # Check if it's a dynamic/JavaScript-heavy page
                    scripts = soup.find_all('script')
                    print(f"\nFound {len(scripts)} script tags (might indicate dynamic content)")
                    
                    # Look for common frameworks
                    page_text = html.lower()
                    frameworks = ['react', 'angular', 'vue', 'jquery']
                    detected = [fw for fw in frameworks if fw in page_text]
                    if detected:
                        print(f"Detected JavaScript frameworks: {', '.join(detected)}")
                        print("Note: This page might require JavaScript rendering")
                    
            except Exception as e:
                print(f"Error examining {url}: {e}")


if __name__ == "__main__":
    asyncio.run(examine_roll20_pages())
