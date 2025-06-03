"""Utilities for parsing incoming email HTML and scraping articles."""

from bs4 import BeautifulSoup
import requests
import os

def extract_fields(html: str) -> dict:
    """Extract expected fields from the incoming email HTML."""
    soup = BeautifulSoup(html, "html.parser")
    mapping = {
        "campaignId": "campaignId",
        "campaignName": "campaignName",
        "articleTitle": "articleTitle",
        "publishingDate": "publishingDate",
        "articleSnippet": "articleSnippet",
        "articleURL": "articleURL",
    }

    fields = {}
    for key, element_id in mapping.items():
        el = soup.find(id=element_id)
        fields[key] = el.get_text(strip=True) if el else None
    return fields

def call_playwright_scraper(url: str) -> str | None:
    """Call a Playwright-based scraping service and return article HTML."""
    api_url = os.environ.get("PLAYWRIGHT_API_URL")
    if not api_url:
        return None
    try:
        resp = requests.post(api_url, json={"url": url}, timeout=30)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return None
