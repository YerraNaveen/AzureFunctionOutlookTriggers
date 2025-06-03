import azure.functions as func
import json
import os
from ..shared.graph_client import send_email

def main(req: func.HttpRequest) -> func.HttpResponse:
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
