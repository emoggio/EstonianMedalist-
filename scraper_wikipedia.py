#!/usr/bin/env python3
"""
Estonia Olympics Results Scraper for Milano Cortina 2026
Main data source: Wikipedia (Estonia at the 2026 Winter Olympics)
URL: https://en.wikipedia.org/wiki/Estonia_at_the_2026_Winter_Olympics
"""

import json
import requests
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Main data source
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Estonia_at_the_2026_Winter_Olympics"

# Wikipedia-friendly headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_url(url, retries=3):
    """Fetch URL with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                import time
                time.sleep(3)
    return None

def extract_medal_count_from_infobox(soup):
    """Extract medal count from Wikipedia infobox"""
    medals = {'gold': 0, 'silver': 0, 'bronze': 0}

    try:
        # Look for infobox with medal counts
        infobox = soup.find('table', class_='infobox')
        if not infobox:
            return medals

        # Find medal rows
        rows = infobox.find_all('tr')
        for row in rows:
            text = row.get_text().lower()

            # Look for gold medals
            if 'gold' in text:
                gold_match = re.search(r'gold[:\s]*(\d+)', text)
                if gold_match:
                    medals['gold'] = int(gold_match.group(1))

            # Look for silver medals
            if 'silver' in text:
                silver_match = re.search(r'silver[:\s]*(\d+)', text)
                if silver_match:
                    medals['silver'] = int(silver_match.group(1))

            # Look for bronze medals
            if 'bronze' in text:
                bronze_match = re.search(r'bronze[:\s]*(\d+)', text)
                if bronze_match:
                    medals['bronze'] = int(bronze_match.group(1))

        # Alternative: Look for medal tally table
        medal_tables = soup.find_all('table', class_='wikitable')
        for table in medal_tables:
            if 'medal' in table.get_text().lower():
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:
                        # Check if this is Estonia's row
                        row_text = row.get_text().lower()
                        if 'estonia' in row_text or 'est' in row_text:
                            try:
                                # Try to extract numbers from cells
                                for i, cell in enumerate(cells):
                                    cell_text = cell.get_text().strip()
                                    if cell_text.isdigit():
                                        num = int(cell_text)
                                        # Typically: Gold, Silver, Bronze, Total
                                        if i == 1 or 'gold' in cells[i].get('class', []):
                                            medals['gold'] = max(medals['gold'], num)
                                        elif i == 2 or 'silver' in cells[i].get('class', []):
                                            medals['silver'] = max(medals['silver'], num)
                                        elif i == 3 or 'bronze' in cells[i].get('class', []):
                                            medals['bronze'] = max(medals['bronze'], num)
                            except:
                                continue

        return medals
    except Exception as e:
        print(f"Error extracting medal count: {e}")
        return medals

def extract_competitors_table(soup):
    """Extract competitors by sport from Wikipedia tables"""
    competitors = []

    try:
        # Look for tables with competitor information
        tables = soup.find_all('table', class_='wikitable')

        for table in tables:
            table_text = table.get_text().lower()

            # Skip medal tables
            if 'medal' in table_text and 'total' in table_text:
                continue

            # Look for tables with athlete names and sports
            rows = table.find_all('tr')
            headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]

            # Check if this table has athlete/sport columns
            has_athlete_col = any('athlete' in h or 'name' in h for h in headers)
            has_sport_col = any('sport' in h or 'event' in h or 'discipline' in h for h in headers)

            if not (has_athlete_col or has_sport_col):
                continue

            for row in rows[1:]:  # Skip header
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    try:
                        # Extract athlete name and sport
                        name = ""
                        sport = ""
                        result = ""
                        medal = None

                        for i, cell in enumerate(cells):
                            cell_text = cell.get_text().strip()

                            # Look for athlete name
                            if i < len(headers) and ('athlete' in headers[i] or 'name' in headers[i]):
                                name = cell_text

                            # Look for sport/event
                            if i < len(headers) and ('sport' in headers[i] or 'event' in headers[i] or 'discipline' in headers[i]):
                                sport = cell_text

                            # Look for results
                            if i < len(headers) and ('result' in headers[i] or 'position' in headers[i] or 'place' in headers[i]):
                                result = cell_text

                            # Check for medal indicators (often in bgcolor or style)
                            cell_style = cell.get('style', '')
                            if 'gold' in cell_style.lower() or '#ffd700' in cell_style.lower():
                                medal = 'gold'
                            elif 'silver' in cell_style.lower() or '#c0c0c0' in cell_style.lower():
                                medal = 'silver'
                            elif 'bronze' in cell_style.lower() or '#cd7f32' in cell_style.lower():
                                medal = 'bronze'

                        # Add competitor if we have at least name or sport
                        if name or sport:
                            competitor = {
                                'name': name,
                                'sport': sport
                            }
                            if result:
                                competitor['result'] = result
                            if medal:
                                competitor['medal'] = medal

                            competitors.append(competitor)
                    except Exception as e:
                        continue

        return competitors
    except Exception as e:
        print(f"Error extracting competitors: {e}")
        return []

def extract_results_from_sections(soup):
    """Extract results from article sections (Alpine skiing, Biathlon, etc.)"""
    results = []

    try:
        # Find all sport sections (h2, h3 headers)
        sections = soup.find_all(['h2', 'h3'])

        for section in sections:
            sport_name = section.get_text().strip()

            # Skip non-sport sections
            skip_sections = ['contents', 'references', 'external links', 'see also', 'notes']
            if any(skip in sport_name.lower() for skip in skip_sections):
                continue

            # Get the next table after this section
            next_table = section.find_next('table', class_='wikitable')
            if not next_table:
                continue

            # Parse the table
            rows = next_table.find_all('tr')
            if len(rows) < 2:
                continue

            # Get headers
            headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]

            # Parse athlete rows
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue

                try:
                    athlete_data = {
                        'sport': sport_name,
                        'name': '',
                        'event': '',
                        'result': ''
                    }

                    for i, cell in enumerate(cells):
                        cell_text = cell.get_text().strip()

                        if i < len(headers):
                            if 'athlete' in headers[i] or 'name' in headers[i]:
                                athlete_data['name'] = cell_text
                            elif 'event' in headers[i]:
                                athlete_data['event'] = cell_text
                            elif 'result' in headers[i] or 'place' in headers[i] or 'rank' in headers[i]:
                                athlete_data['result'] = cell_text
                            elif 'date' in headers[i]:
                                athlete_data['date'] = cell_text

                        # Check for medal styling
                        cell_style = cell.get('style', '').lower()
                        cell_bgcolor = cell.get('bgcolor', '').lower()

                        if 'gold' in cell_style or '#ffd700' in cell_style or 'gold' in cell_bgcolor:
                            athlete_data['medal'] = 'gold'
                        elif 'silver' in cell_style or '#c0c0c0' in cell_style or 'silver' in cell_bgcolor:
                            athlete_data['medal'] = 'silver'
                        elif 'bronze' in cell_style or '#cd7f32' in cell_style or 'bronze' in cell_bgcolor:
                            athlete_data['medal'] = 'bronze'

                    if athlete_data['name'] or athlete_data['event']:
                        results.append(athlete_data)

                except Exception as e:
                    continue

        return results
    except Exception as e:
        print(f"Error extracting results from sections: {e}")
        return []

def merge_athlete_data(existing_data, new_athletes):
    """Merge new athlete data with existing data.json"""
    # This is a conservative merge - we don't want to overwrite manual updates
    # Only update medal counts automatically

    completed = existing_data.get('completed', [])
    upcoming = existing_data.get('upcoming', [])

    # Track athlete names we already have
    existing_names = set()
    for athlete in completed + upcoming:
        existing_names.add(athlete.get('name', '').lower())

    # Add new athletes if they're not already tracked
    new_completed = []
    for athlete in new_athletes:
        name = athlete.get('name', '').lower()

        # Skip if we already have this athlete
        if name in existing_names or not name:
            continue

        # If athlete has a result, add to completed
        if athlete.get('result') or athlete.get('medal'):
            new_completed.append({
                'name': athlete.get('name', ''),
                'sport': athlete.get('sport', '') + (f" - {athlete.get('event', '')}" if athlete.get('event') else ''),
                'result': athlete.get('result', ''),
                'medal': athlete.get('medal')
            })

    return new_completed

def update_data_from_wikipedia():
    """Main function to update data from Wikipedia"""
    print(f"Starting Wikipedia Olympics scraper at {datetime.utcnow().isoformat()}")
    print(f"Data source: {WIKIPEDIA_URL}")

    # Load current data
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        current_data = {
            "medals": {"gold": 0, "silver": 0, "bronze": 0},
            "completed": [],
            "upcoming": []
        }

    print(f"Current medals: Gold: {current_data['medals']['gold']}, "
          f"Silver: {current_data['medals']['silver']}, "
          f"Bronze: {current_data['medals']['bronze']}")

    # Fetch Wikipedia page
    page_content = fetch_url(WIKIPEDIA_URL)

    if not page_content:
        print("Failed to fetch Wikipedia page. Keeping existing data.")
        return

    # Parse with BeautifulSoup
    soup = BeautifulSoup(page_content, 'lxml')

    # Extract medal count from infobox
    medals = extract_medal_count_from_infobox(soup)
    print(f"Scraped medals: Gold: {medals['gold']}, Silver: {medals['silver']}, Bronze: {medals['bronze']}")

    # Extract competitor information
    competitors = extract_competitors_table(soup)
    results = extract_results_from_sections(soup)

    all_athletes = competitors + results
    print(f"Found {len(all_athletes)} athlete entries on Wikipedia")

    # Log what we found
    for athlete in all_athletes[:10]:  # Show first 10
        print(f"  - {athlete.get('name', 'Unknown')}: {athlete.get('sport', 'Unknown sport')}")
        if athlete.get('result'):
            print(f"    Result: {athlete.get('result')}")
        if athlete.get('medal'):
            print(f"    Medal: {athlete.get('medal')}")

    # Update medal counts if they changed
    old_medal_total = sum(current_data['medals'].values())
    new_medal_total = sum(medals.values())

    if new_medal_total > old_medal_total:
        print("\n🏅 NEW MEDALS DETECTED! 🏅")
        current_data['medals'] = medals
    elif new_medal_total < old_medal_total:
        print("\n⚠️ Warning: Medal count decreased. Keeping existing count to prevent data loss.")
    else:
        print("No change in medal count.")
        current_data['medals'] = medals  # Update anyway to ensure consistency

    # Merge new athlete data (conservative approach)
    new_completed_athletes = merge_athlete_data(current_data, all_athletes)

    if new_completed_athletes:
        print(f"\nFound {len(new_completed_athletes)} new athletes to add:")
        for athlete in new_completed_athletes:
            print(f"  + {athlete['name']}: {athlete['sport']}")

    # Note: We don't automatically add athletes to preserve manual updates
    # Operators should review Wikipedia and update data.json manually for athlete details

    # Write updated data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print(f"Update complete!")
    print(f"Total medals: {sum(current_data['medals'].values())}")
    print(f"Athletes tracked: {len(current_data.get('completed', []))} completed, "
          f"{len(current_data.get('upcoming', []))} upcoming")
    print("\nData source: Wikipedia (Estonia at the 2026 Winter Olympics)")
    print(f"URL: {WIKIPEDIA_URL}")
    print("\nNote: Athlete details should be manually verified and updated in data.json")

if __name__ == "__main__":
    update_data_from_wikipedia()
