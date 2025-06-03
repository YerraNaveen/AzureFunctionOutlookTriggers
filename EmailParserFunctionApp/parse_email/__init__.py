import azure.functions as func
import json
import os
from ..shared.parser_utils import extract_fields, call_playwright_scraper
from ..shared.graph_client import send_email

def main(req: func.HttpRequest) -> func.HttpResponse:
    route = req.route_params.get('route') or req.url.split('/')[-1]
    if route == 'parse-email':
        return parse_email(req)
    elif route == 'handle-playwright-failure':
        return handle_playwright_failure(req)
    elif route == 'handle-gpt-filter-failure':
        return handle_gpt_filter_failure(req)
    elif route == 'handle-relevance-failure':
        return handle_relevance_failure(req)
    elif route == 'final-delivery':
        return final_delivery(req)
    return func.HttpResponse('Not found', status_code=404)

def parse_email(req):
    try:
        data = req.get_json()
        html = data.get('html')
        fields = extract_fields(html)
        article_url = fields.get('articleUrl')
        scraped_html = call_playwright_scraper(article_url)
        if not scraped_html:
            return func.HttpResponse(json.dumps({'error': 'Scraping failed', 'fields': fields}), status_code=428, mimetype='application/json')
        fields['scraped_html'] = scraped_html
        return func.HttpResponse(json.dumps(fields), mimetype='application/json')
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)

def handle_playwright_failure(req):
    data = req.get_json()
    fields = data.get('fields', {})
    subject = f"[Fallback] Scraping failed for {fields.get('articleTitle', 'article')}"
    body = f"Scraping failed. Manual review needed.\n<br>Fields: {json.dumps(fields)}"
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    send_email(subject, body, to, importance='normal')
    return func.HttpResponse('Fallback email sent', status_code=200)

def handle_gpt_filter_failure(req):
    data = req.get_json()
    fields = data.get('fields', {})
    subject = f"[Fallback] GPT filter blocked {fields.get('articleTitle', 'article')}"
    body = f"Content blocked by GPT filter.\n<br>Fields: {json.dumps(fields)}"
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    send_email(subject, body, to, importance='normal')
    return func.HttpResponse('Fallback email sent', status_code=200)

def handle_relevance_failure(req):
    data = req.get_json()
    fields = data.get('fields', {})
    subject = f"[Non-SLT] {fields.get('articleTitle', 'article')}"
    body = f"Article marked as non-SLT-relevant.\n<br>Fields: {json.dumps(fields)}"
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    send_email(subject, body, to, importance='normal')
    return func.HttpResponse('Non-SLT fallback email sent', status_code=200)

def final_delivery(req):
    data = req.get_json()
    fields = data.get('fields', {})
    subject = fields.get('articleTitle', 'Article')
    body = fields.get('scraped_html', '')
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    campaign = fields.get('campaignName', '') or ''
    title = fields.get('articleTitle', '') or ''
    importance = 'high' if ('slt' in campaign.lower() or 'slt' in title.lower()) else 'normal'
    send_email(subject, body, to, importance=importance)
    return func.HttpResponse('Final email sent', status_code=200)
