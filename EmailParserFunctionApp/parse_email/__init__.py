import azure.functions as func
import json
from ..shared.parser_utils import extract_fields, call_playwright_scraper

def main(req: func.HttpRequest) -> func.HttpResponse:
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
