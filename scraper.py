#!/usr/bin/env python3
"""
Estonia Olympics Results Scraper for Milano Cortina 2026
Fetches medal counts from Olympics.com and updates data.json
Athlete data must be manually updated
"""

import json
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
import sys
import os

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# URLs to scrape
ESTONIA_MEDALS_URL = "https://www.olympics.com/en/milano-cortina-2026/medals/est"
MEDALS_TABLE_URL = "https://www.olympics.com/en/milano-cortina-2026/medals"

# User agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def fetch_page(url, retries=3):
    """Fetch a page with retries using requests"""
    for attempt in range(retries):
        try:
            session = requests.Session()
            response = session.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                print(f"Failed to fetch {url} after {retries} attempts")
                return None

def parse_medal_count(html):
    """Parse medal counts from the medals page"""
    medals = {"gold": 0, "silver": 0, "bronze": 0}

    if not html:
        return None

    try:
        soup = BeautifulSoup(html, 'lxml')

        # Strategy 1: Look for Estonia in medal table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                text = row.get_text(strip=True)

                # Look for Estonia row
                if 'Estonia' in text or 'EST' in text or 'Eesti' in text:
                    # Try to extract numbers from the row
                    cells = row.find_all(['td', 'th'])

                    # Try to find cells with numbers
                    numbers = []
                    for cell in cells:
                        cell_text = cell.get_text(strip=True)
                        if cell_text.isdigit():
                            numbers.append(int(cell_text))

                    # Medal table usually has: Rank, Country, Gold, Silver, Bronze, Total
                    if len(numbers) >= 4:
                        # Skip rank (first number) and total (last number), take middle 3
                        if len(numbers) == 5:  # rank, gold, silver, bronze, total
                            medals['gold'] = numbers[1]
                            medals['silver'] = numbers[2]
                            medals['bronze'] = numbers[3]
                            print(f"Found medals in table format 1: {medals}")
                            return medals
                        elif len(numbers) == 4:  # gold, silver, bronze, total
                            medals['gold'] = numbers[0]
                            medals['silver'] = numbers[1]
                            medals['bronze'] = numbers[2]
                            print(f"Found medals in table format 2: {medals}")
                            return medals

        # Strategy 2: Look for any numbers near "Estonia" text
        # Find all text containing Estonia
        for elem in soup.find_all(string=re.compile(r'Estonia|EST|Eesti', re.I)):
            parent = elem.find_parent()
            if parent:
                # Look for numbers in parent and siblings
                for sibling in parent.find_next_siblings(limit=10):
                    numbers = re.findall(r'\b\d+\b', sibling.get_text())
                    if len(numbers) >= 3:
                        try:
                            medals['gold'] = int(numbers[0])
                            medals['silver'] = int(numbers[1])
                            medals['bronze'] = int(numbers[2])
                            print(f"Found medals near Estonia text: {medals}")
                            return medals
                        except (ValueError, IndexError):
                            continue

        # Strategy 3: Look for medal count containers
        medal_containers = soup.find_all(['div', 'span', 'td'],
                                        class_=re.compile(r'medal.*count|gold|silver|bronze', re.I))

        for container in medal_containers:
            text = container.get_text(strip=True)
            if text.isdigit():
                # This might be a medal count
                pass

        print("Could not parse medal count from page")
        return None

    except Exception as e:
        print(f"Error parsing medal count: {e}")
        return None

def load_current_data():
    """Load existing data from file"""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No existing data.json found - creating default structure")
        return {
            "medals": {"gold": 0, "silver": 0, "bronze": 0},
            "completed": [],
            "upcoming": []
        }

def main():
    """Main scraper function"""
    print(f"Starting Estonia Olympics medal scraper at {datetime.utcnow().isoformat()}")
    print("Note: This scraper only updates medal counts. Athlete data must be manually updated.")

    # Load current data
    current_data = load_current_data()

    old_total = (current_data['medals']['gold'] +
                 current_data['medals']['silver'] +
                 current_data['medals']['bronze'])

    print(f"Current medals: Gold: {current_data['medals']['gold']}, "
          f"Silver: {current_data['medals']['silver']}, "
          f"Bronze: {current_data['medals']['bronze']}")

    # Try to fetch medal counts from multiple URLs
    print("Fetching medal counts from Olympics.com...")

    medal_html = fetch_page(ESTONIA_MEDALS_URL)

    if not medal_html:
        print("Trying alternate medals URL...")
        medal_html = fetch_page(MEDALS_TABLE_URL)

    if medal_html:
        medals = parse_medal_count(medal_html)

        if medals:
            # Check if medals increased
            new_total = medals['gold'] + medals['silver'] + medals['bronze']

            if new_total > old_total:
                print(f"MEDALS UPDATED! New medals: Gold: {medals['gold']}, "
                      f"Silver: {medals['silver']}, Bronze: {medals['bronze']}")
                current_data['medals'] = medals
            elif new_total == old_total and medals != current_data['medals']:
                # Medal composition changed (e.g., traded a silver for a gold)
                print(f"Medal composition changed: {medals}")
                current_data['medals'] = medals
            else:
                print("No medal changes detected")
        else:
            print("Could not parse medals from page. Keeping existing data.")
    else:
        print("Could not fetch medal pages. Keeping existing data.")

    # Write updated data (even if unchanged, to verify workflow is running)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    total_medals = current_data['medals']['gold'] + current_data['medals']['silver'] + current_data['medals']['bronze']
    print(f"Update complete! Total medals: {total_medals}")
    print(f"Athletes: {len(current_data.get('completed', []))} completed, "
          f"{len(current_data.get('upcoming', []))} upcoming")
    print("\nTo update athlete data:")
    print("1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/edit/main/data.json")
    print("2. Move athletes from 'upcoming' to 'completed' and add results")
    print("3. Commit changes")

if __name__ == "__main__":
    main()
