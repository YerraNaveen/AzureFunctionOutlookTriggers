import azure.functions as func
import json
import os
from ..shared.graph_client import send_email

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    fields = data.get('fields', {})
    subject = f"[Non-SLT] {fields.get('articleTitle', 'article')}"
    to = os.environ.get('SLT_RECIPIENT_EMAIL')
    send_email(subject, fields, to, '', importance='normal')
    return func.HttpResponse('Non-SLT fallback email sent', status_code=200)
