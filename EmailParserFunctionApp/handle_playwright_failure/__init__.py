import azure.functions as func
import json
import os
from ..shared.graph_client import send_email

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    fields = data.get('fields', {})
    subject = f"[Fallback] Scraping failed for {fields.get('articleTitle', 'article')}"
    body = f"Scraping failed. Manual review needed.\n<br>Fields: {json.dumps(fields)}"
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    send_email(subject, body, to, importance='normal')
    return func.HttpResponse('Fallback email sent', status_code=200)
