#!/usr/bin/env python3
"""
Estonia Olympics Results Scraper for Milano Cortina 2026
Uses ERR (Estonian Public Broadcasting) RSS feed and website
Data source: https://sport.err.ee
"""

import json
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import sys
from datetime import datetime

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Data sources
ERR_RSS_FEED = "https://sport.err.ee/rss"
ERR_OLYMPICS_PAGE = "https://sport.err.ee/k/om2026"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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

def parse_err_rss_feed():
    """Parse ERR RSS feed for Olympics news"""
    print("Fetching ERR RSS feed...")
    rss_content = fetch_url(ERR_RSS_FEED)

    if not rss_content:
        return []

    try:
        root = ET.fromstring(rss_content)
        articles = []

        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''

            # Filter for Olympics content
            olympics_keywords = ['olümpia', 'olympics', 'milano', 'cortina', 'om2026']
            if any(keyword in title.lower() or keyword in description.lower() for keyword in olympics_keywords):
                articles.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'pub_date': pub_date
                })

        print(f"Found {len(articles)} Olympics articles in RSS feed")
        return articles

    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        return []

def extract_medal_info(text):
    """Extract ESTONIAN medal information from text"""
    medals = {'gold': 0, 'silver': 0, 'bronze': 0}

    text_lower = text.lower()

    # First check if this is about Estonia - must have Estonian athlete names or "eesti" keyword
    estonian_markers = ['eesti', 'estonia', 'est', 'talihärm', 'kulbin', 'sildaru', 'ilves',
                       'ermits', 'kuelm', 'tomingas', 'siimer', 'kehva', 'zahkna', 'teder',
                       'laine', 'meentalo', 'kaasiku', 'pulles', 'tuul', 'ojaste', 'alev',
                       'dremljuga', 'himma', 'kaldvee', 'lill', 'selevko', 'liiv', 'zunte']

    has_estonian_context = any(marker in text_lower for marker in estonian_markers)

    if not has_estonian_context:
        return medals  # Not about Estonia, return zeros

    # Estonian medal keywords - must co-occur with Estonian context
    medal_patterns = [
        # Estonian patterns
        (r'eesti.*?kuldmedal', 'gold'),
        (r'eesti.*?hõbemedal', 'silver'),
        (r'eesti.*?pronksmedal', 'bronze'),
        (r'kuldmedal.*?eesti', 'gold'),
        (r'hõbemedal.*?eesti', 'silver'),
        (r'pronksmedal.*?eesti', 'bronze'),
        (r'võitis kulla', 'gold'),
        (r'võitis hõbeda', 'silver'),
        (r'võitis pronksi', 'bronze'),
        # English patterns with Estonia
        (r'estonia.*?gold medal', 'gold'),
        (r'estonia.*?silver medal', 'silver'),
        (r'estonia.*?bronze medal', 'bronze'),
        (r'gold medal.*?estonia', 'gold'),
        (r'silver medal.*?estonia', 'silver'),
        (r'bronze medal.*?estonia', 'bronze'),
    ]

    for pattern, medal_type in medal_patterns:
        if re.search(pattern, text_lower):
            medals[medal_type] += 1

    return medals

def extract_athlete_result(text, title):
    """Extract athlete results from article text"""
    # Look for placement patterns
    placement_patterns = [
        r'(\d+)\.\s*koht',  # Estonian: "6. koht" = 6th place
        r'place\s*(\d+)',
        r'finished\s*(\d+)',
        r'(\d+)th place'
    ]

    for pattern in placement_patterns:
        match = re.search(pattern, text.lower())
        if match:
            return f"{match.group(1)}th place"

    # Check for DNF, DQ, etc.
    if any(keyword in text.lower() for keyword in ['katkestas', 'did not finish', 'dnf', 'diskvalifitseeriti']):
        return "Did not finish"

    return None

def parse_olympics_page():
    """Parse ERR Olympics dedicated page for detailed results"""
    print("Fetching ERR Olympics page...")
    page_content = fetch_url(ERR_OLYMPICS_PAGE)

    if not page_content:
        return []

    try:
        soup = BeautifulSoup(page_content, 'lxml')

        results = []

        # Find all article links and headlines
        articles = soup.find_all(['article', 'h2', 'h3', 'a'], class_=re.compile(r'article|headline|title|link'))

        for article in articles:
            try:
                # Get article text and link
                text = article.get_text(strip=True)
                link = article.get('href', '')

                # Ensure full URL
                if link and not link.startswith('http'):
                    link = f"https://sport.err.ee{link}"

                # Skip if too short
                if len(text) < 10:
                    continue

                # Check for Estonian athlete names or keywords
                estonian_markers = ['eesti', 'külm', 'külm', 'ermits', 'talihärm', 'tomingas',
                                   'ilves', 'kulbin', 'sildaru', 'siimer', 'kehva', 'zahkna',
                                   'teder', 'laine', 'meentalo', 'kaasiku', 'pulles', 'tuul',
                                   'ojaste', 'alev', 'dremljuga', 'himma', 'kaldvee', 'lill',
                                   'selevko', 'liiv', 'zunte', 'aigro']

                has_estonian = any(marker in text.lower() for marker in estonian_markers)

                if has_estonian:
                    # Extract result information
                    result_info = {
                        'text': text,
                        'link': link,
                        'placement': extract_athlete_result(text, text),
                        'medals': extract_medal_info(text)
                    }

                    results.append(result_info)
                    print(f"Found Estonian content: {text[:80]}...")

            except Exception as e:
                continue

        print(f"Extracted {len(results)} Estonian-related items from Olympics page")
        return results

    except Exception as e:
        print(f"Error parsing Olympics page: {e}")
        return []

def update_data_from_err():
    """Main function to update data from ERR sources"""
    print(f"Starting ERR Olympics scraper at {datetime.utcnow().isoformat()}")
    print("Data source: ERR (Estonian Public Broadcasting)")

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

    # Parse RSS feed
    articles = parse_err_rss_feed()

    # Check for medal mentions in recent articles
    total_medals = {'gold': 0, 'silver': 0, 'bronze': 0}
    athlete_updates = []

    for article in articles[:20]:  # Check last 20 articles
        # Check for medal info
        text = article['title'] + ' ' + article['description']
        medals = extract_medal_info(text)

        for medal_type in ['gold', 'silver', 'bronze']:
            total_medals[medal_type] += medals[medal_type]

        # Extract athlete results
        result = extract_athlete_result(text, article['title'])
        if result:
            athlete_updates.append({
                'article': article['title'],
                'result': result,
                'link': article['link']
            })

    # Update medal counts if found
    if sum(total_medals.values()) > 0:
        print(f"Found medal mentions: {total_medals}")
        # Only update if medals increased
        old_total = sum(current_data['medals'].values())
        new_total = sum(total_medals.values())

        if new_total > old_total:
            print("MEDALS UPDATED!")
            current_data['medals'] = total_medals

    # Display athlete updates found
    if athlete_updates:
        print("\nRecent athlete results found:")
        for update in athlete_updates:
            print(f"  - {update['article']}: {update['result']}")
            print(f"    Link: {update['link']}")

    # Parse Olympics page for additional context and results
    print("\n" + "="*60)
    olympics_page_results = parse_olympics_page()

    if olympics_page_results:
        print(f"\nProcessing {len(olympics_page_results)} items from Olympics page...")

        # Check for additional medal info
        for item in olympics_page_results:
            item_medals = item.get('medals', {})
            for medal_type in ['gold', 'silver', 'bronze']:
                if item_medals.get(medal_type, 0) > 0:
                    print(f"Found {medal_type} medal mention: {item['text'][:100]}")
                    total_medals[medal_type] += item_medals[medal_type]

            # Log any placement info found
            if item.get('placement'):
                print(f"  Result found: {item['placement']} - {item['link']}")

        # Update medals if new ones found
        if sum(total_medals.values()) > sum(current_data['medals'].values()):
            print("\nNEW MEDALS DETECTED from Olympics page!")
            current_data['medals'] = total_medals

    # Write updated data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print(f"Update complete!")
    print(f"Total medals: {sum(current_data['medals'].values())}")
    print(f"Athletes: {len(current_data.get('completed', []))} completed, "
          f"{len(current_data.get('upcoming', []))} upcoming")
    print("\nData sources checked:")
    print(f"  - ERR RSS Feed: {len(articles)} Olympics articles")
    print(f"  - ERR Olympics Page: {len(olympics_page_results)} Estonian items")
    print("\nFor detailed results, see:")
    print("  ERR Olympics: https://sport.err.ee/k/om2026")
    print("  ERR RSS: https://sport.err.ee/rss")

if __name__ == "__main__":
    update_data_from_err()
