from bs4 import BeautifulSoup
import requests
import os

def extract_fields(html):
    """Extracts fields from HTML by ID using BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    fields = {}
    # Example: extract fields by ID (customize as needed)
    for field_id in ['campaignName', 'articleTitle', 'articleUrl', 'articleDate']:
        el = soup.find(id=field_id)
        fields[field_id] = el.get_text(strip=True) if el else None
    return fields

def call_playwright_scraper(url):
    """Calls Playwright API to scrape the article. Returns HTML or None on failure."""
    api_url = os.environ.get('PLAYWRIGHT_API_URL')
    if not api_url:
        return None
    try:
        resp = requests.post(api_url, json={"url": url}, timeout=30)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return None
