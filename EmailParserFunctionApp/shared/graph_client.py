"""Microsoft Graph email utilities."""

import os
import requests
from .email_template import build_email_html


def get_graph_token() -> str:
    tenant = os.environ.get("TENANT_ID")
    client_id = os.environ.get("CLIENT_ID")
    secret = os.environ.get("CLIENT_SECRET")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": secret,
        "scope": "https://graph.microsoft.com/.default",
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def send_email(fields: dict, article_html: str, importance: str = "normal") -> int:
    """Send an email via Microsoft Graph."""
    token = get_graph_token()
    sender = os.environ.get("SENDER_EMAIL")
    recipient = os.environ.get("SLT_RECIPIENT_EMAIL")
    graph_url = f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    html_body = build_email_html(fields, article_html)
    subject = fields.get("articleTitle", "Article")
    message = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": html_body},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
            "importance": importance,
        }
    }
    resp = requests.post(graph_url, headers=headers, json=message)
    resp.raise_for_status()
    return resp.status_code


def handle_scrape_failure(fields: dict) -> None:
    fields = dict(fields)
    fields["articleTitle"] = f"{fields.get('articleTitle', 'Article')} - Manual Intervention Needed"
    send_email(fields, "", "normal")


def handle_gpt_filter_failure(fields: dict) -> None:
    fields = dict(fields)
    fields["articleTitle"] = f"{fields.get('articleTitle', 'Article')} - Manual Intervention Needed"
    send_email(fields, "", "normal")


def handle_relevance_failure(fields: dict, html: str) -> None:
    send_email(fields, html, "normal")


def send_final_email(fields: dict, html: str, importance: str = "high") -> None:
    send_email(fields, html, importance)
