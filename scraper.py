#!/usr/bin/env python3
"""
Estonia Olympics Results Scraper for Milano Cortina 2026
Fetches real-time results from Olympics.com and updates data.json
"""

import json
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re

# URLs to scrape
ESTONIA_SCHEDULE_URL = "https://www.olympics.com/en/milano-cortina-2026/schedule/est"
ESTONIA_PROFILE_URL = "https://www.olympics.com/en/milano-cortina-2026/results/noc-profile/est"
ESTONIA_MEDALS_URL = "https://www.olympics.com/en/milano-cortina-2026/medals/est"

# User agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def fetch_page(url, retries=3):
    """Fetch a page with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(3)
            else:
                print(f"Failed to fetch {url} after {retries} attempts")
                return None

def parse_medal_count(html):
    """Parse medal counts from the page"""
    medals = {"gold": 0, "silver": 0, "bronze": 0}

    if not html:
        return medals

    try:
        soup = BeautifulSoup(html, 'lxml')

        # Try multiple strategies to find medal counts
        # Strategy 1: Look for medal table cells
        medal_cells = soup.find_all('td', class_=re.compile(r'medal', re.I))

        # Strategy 2: Look for specific medal count elements
        gold_elem = soup.find(string=re.compile(r'gold', re.I))
        if gold_elem:
            parent = gold_elem.find_parent()
            if parent:
                numbers = re.findall(r'\d+', parent.get_text())
                if numbers:
                    medals['gold'] = int(numbers[0])

        # Strategy 3: Parse table structure
        medal_table = soup.find('table', class_=re.compile(r'medal', re.I))
        if medal_table:
            rows = medal_table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:
                    try:
                        medals['gold'] = int(cells[1].get_text(strip=True))
                        medals['silver'] = int(cells[2].get_text(strip=True))
                        medals['bronze'] = int(cells[3].get_text(strip=True))
                        break
                    except (ValueError, IndexError):
                        continue

    except Exception as e:
        print(f"Error parsing medal count: {e}")

    return medals

def parse_schedule_and_results(schedule_html, profile_html):
    """Parse schedule to determine completed vs upcoming events"""
    completed = []
    upcoming = []

    if not schedule_html and not profile_html:
        return None, None

    try:
        # Parse the schedule page
        soup = BeautifulSoup(schedule_html or profile_html, 'lxml')

        # Look for athlete entries, event listings, or competition cards
        # This is a heuristic parser - Olympics.com structure may vary

        # Try to find competition units or event cards
        events = soup.find_all(['div', 'article', 'section'],
                               class_=re.compile(r'(event|competition|unit|schedule)', re.I))

        print(f"Found {len(events)} potential event elements")

        # If we can't parse the dynamic structure, return None to keep existing data
        if not events:
            print("No events found - keeping existing athlete data")
            return None, None

        # Parse events and categorize them
        for event in events[:50]:  # Limit to avoid processing too much
            try:
                # Extract athlete name, sport, date, result
                text = event.get_text(strip=True)

                # Look for Estonian athlete names or "EST" markers
                if 'EST' in text or any(name in text for name in ['Sildaru', 'Talihärm', 'Kaldvee', 'Lill']):
                    print(f"Found potential Estonian event: {text[:100]}")
                    # More parsing logic would go here

            except Exception as e:
                continue

        # Since Olympics.com has dynamic content, return None to preserve manual data
        print("Keeping manually curated athlete data - automatic parsing not reliable yet")
        return None, None

    except Exception as e:
        print(f"Error parsing schedule/results: {e}")
        return None, None

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
    print(f"🏔️ Starting Estonia Olympics scraper at {datetime.utcnow().isoformat()}")

    # Load current data
    current_data = load_current_data()

    print(f"Current data: {len(current_data.get('completed', []))} completed, "
          f"{len(current_data.get('upcoming', []))} upcoming")

    # Fetch medal counts (most reliable data)
    print("📊 Fetching medal counts...")
    medal_html = fetch_page(ESTONIA_MEDALS_URL)
    medals = parse_medal_count(medal_html)

    # Always update medal counts if we got valid data
    if medals and (medals['gold'] > 0 or medals['silver'] > 0 or medals['bronze'] > 0):
        current_data['medals'] = medals
        print(f"Updated medals: 🥇{medals['gold']} 🥈{medals['silver']} 🥉{medals['bronze']}")
    else:
        # Keep existing medal counts if scraping failed
        print(f"Keeping existing medals: 🥇{current_data['medals']['gold']} "
              f"🥈{current_data['medals']['silver']} 🥉{current_data['medals']['bronze']}")

    # Try to fetch athlete schedule/results
    print("👥 Fetching athlete schedule and results...")
    schedule_html = fetch_page(ESTONIA_SCHEDULE_URL)
    profile_html = fetch_page(ESTONIA_PROFILE_URL)

    completed, upcoming = parse_schedule_and_results(schedule_html, profile_html)

    # Only update athlete lists if we successfully parsed them
    # Otherwise keep the manually curated data
    if completed is not None and upcoming is not None:
        current_data['completed'] = completed
        current_data['upcoming'] = upcoming
        print(f"Updated athletes: {len(completed)} completed, {len(upcoming)} upcoming")
    else:
        print("Preserving manually curated athlete data")

    # Write updated data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    total_medals = current_data['medals']['gold'] + current_data['medals']['silver'] + current_data['medals']['bronze']
    print(f"✅ Update complete! Total medals: {total_medals}")
    print(f"   Athletes: {len(current_data.get('completed', []))} completed, "
          f"{len(current_data.get('upcoming', []))} upcoming")

if __name__ == "__main__":
    main()
