import json
import logging
from bs4 import BeautifulSoup
import azure.functions as func

from ..shared.parser_utils import extract_fields, call_playwright_scraper
from ..shared.gpt_stub import gpt_html_filter_check, gpt_relevance_check
from ..shared.graph_client import (
    handle_scrape_failure,
    handle_gpt_filter_failure,
    handle_relevance_failure,
    send_final_email,
)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("/parse-email endpoint triggered")

    try:
        data = req.get_json()
    except ValueError:
        logging.error("Invalid JSON payload")
        return func.HttpResponse("Invalid JSON", status_code=400)

    html = data.get("html")
    if not html:
        return func.HttpResponse("Missing 'html' in request", status_code=400)

    fields = extract_fields(html)
    article_url = fields.get("articleURL")

    scraped_html = None
    if article_url:
        scraped_html = call_playwright_scraper(article_url)
    if not scraped_html:
        handle_scrape_failure(fields)
        return func.HttpResponse(json.dumps({"status": "scraping_failed"}), mimetype="application/json")

    if not gpt_html_filter_check(scraped_html):
        handle_gpt_filter_failure(fields)
        return func.HttpResponse(json.dumps({"status": "gpt_filtered"}), mimetype="application/json")

    clean_text = BeautifulSoup(scraped_html, "html.parser").get_text(separator=" ", strip=True)
    if not gpt_relevance_check(clean_text):
        handle_relevance_failure(fields, scraped_html)
        return func.HttpResponse(json.dumps({"status": "not_relevant"}), mimetype="application/json")

    send_final_email(fields, scraped_html, importance="high")
    return func.HttpResponse(json.dumps({"status": "email_sent", "importance": "high"}), mimetype="application/json")
