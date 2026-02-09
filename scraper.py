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

# URLs to scrape
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
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2)
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

        # Try to find medal counts - structure may vary
        # Looking for medal table or medal summary elements
        medal_elements = soup.find_all(['span', 'div', 'td'], class_=lambda x: x and 'medal' in x.lower())

        for elem in medal_elements:
            text = elem.get_text(strip=True).lower()
            # Extract numbers from medal-related elements
            if 'gold' in text or 'gold' in str(elem.get('class', [])).lower():
                try:
                    medals['gold'] = int(''.join(filter(str.isdigit, text))) or 0
                except:
                    pass
            elif 'silver' in text or 'silver' in str(elem.get('class', [])).lower():
                try:
                    medals['silver'] = int(''.join(filter(str.isdigit, text))) or 0
                except:
                    pass
            elif 'bronze' in text or 'bronze' in str(elem.get('class', [])).lower():
                try:
                    medals['bronze'] = int(''.join(filter(str.isdigit, text))) or 0
                except:
                    pass
    except Exception as e:
        print(f"Error parsing medal count: {e}")

    return medals

def parse_athletes(html):
    """Parse athlete information from the page"""
    completed = []
    upcoming = []

    if not html:
        return completed, upcoming

    try:
        soup = BeautifulSoup(html, 'lxml')

        # This is a simplified parser - the actual structure may vary
        # We'll look for athlete cards, rows, or list items
        athlete_elements = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and ('athlete' in str(x).lower() or 'competitor' in str(x).lower()))

        # If we don't find specific athlete elements, fall back to searching for names
        if not athlete_elements:
            # Keep the current data structure as fallback
            return None, None

    except Exception as e:
        print(f"Error parsing athletes: {e}")
        return None, None

    return completed, upcoming

def get_default_data():
    """Return default Estonia Olympic data structure"""
    return {
        "medals": {
            "gold": 0,
            "silver": 0,
            "bronze": 0
        },
        "completed": [
            {
                "name": "Marie Kaldvee & Harri Lill",
                "sport": "Curling - Mixed Doubles"
            }
        ],
        "upcoming": [
            {"name": "Johanna Talihärm", "sport": "Biathlon"},
            {"name": "Regina Ermits", "sport": "Biathlon"},
            {"name": "Susan Kuelm", "sport": "Biathlon"},
            {"name": "Tuuli Tomingas", "sport": "Biathlon"},
            {"name": "Jakob Kulbin", "sport": "Biathlon"},
            {"name": "Kristo Siimer", "sport": "Biathlon"},
            {"name": "Mark-Markos Kehva", "sport": "Biathlon"},
            {"name": "Rene Zahkna", "sport": "Biathlon"},
            {"name": "Hanna Gret Teder", "sport": "Alpine Skiing"},
            {"name": "Tormis Laine", "sport": "Alpine Skiing"},
            {"name": "Kelly Sildaru", "sport": "Freestyle Skiing"},
            {"name": "Grete-Mia Meentalo", "sport": "Freestyle Skiing"},
            {"name": "Henry Sildaru", "sport": "Freestyle Skiing"},
            {"name": "Kaidy Kaasiku", "sport": "Cross-Country Skiing"},
            {"name": "Keidy Kaasiku", "sport": "Cross-Country Skiing"},
            {"name": "Mariel Merlii Pulles", "sport": "Cross-Country Skiing"},
            {"name": "Teesi Tuul", "sport": "Cross-Country Skiing"},
            {"name": "Teiloora Ojaste", "sport": "Cross-Country Skiing"},
            {"name": "Alvar Johannes Alev", "sport": "Cross-Country Skiing"},
            {"name": "Karl Sebastian Dremljuga", "sport": "Cross-Country Skiing"},
            {"name": "Martin Himma", "sport": "Cross-Country Skiing"}
        ]
    }

def main():
    """Main scraper function"""
    print(f"🏔️ Starting Estonia Olympics scraper at {datetime.utcnow().isoformat()}")

    # Load current data
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        current_data = get_default_data()

    # Fetch medal counts
    print("📊 Fetching medal counts...")
    medal_html = fetch_page(ESTONIA_MEDALS_URL)
    medals = parse_medal_count(medal_html)

    # Update medal counts
    current_data['medals'] = medals

    # Fetch athlete information
    print("👥 Fetching athlete information...")
    profile_html = fetch_page(ESTONIA_PROFILE_URL)
    completed, upcoming = parse_athletes(profile_html)

    # Only update athlete lists if we successfully parsed them
    if completed is not None:
        current_data['completed'] = completed
    if upcoming is not None:
        current_data['upcoming'] = upcoming

    # Write updated data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    total_medals = medals['gold'] + medals['silver'] + medals['bronze']
    print(f"✅ Update complete! Total medals: {total_medals} (🥇{medals['gold']} 🥈{medals['silver']} 🥉{medals['bronze']})")

if __name__ == "__main__":
    main()
