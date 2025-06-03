# Utilities for Microsoft Graph email

import os
import requests

def get_graph_token():
    tenant_id = os.environ.get('TENANT_ID')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()['access_token']

def send_email(subject, body, to, importance='normal'):
    token = get_graph_token()
    sender = os.environ.get('SENDER_EMAIL')
    url = 'https://graph.microsoft.com/v1.0/users/{}/sendMail'.format(sender)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    message = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'HTML',
                'content': body
            },
            'toRecipients': [{'emailAddress': {'address': to}}],
            'importance': importance
        }
    }
    resp = requests.post(url, headers=headers, json=message)
    resp.raise_for_status()
    return resp.status_code
