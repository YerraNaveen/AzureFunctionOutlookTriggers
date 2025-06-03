# Azure Function App: Meltwater Email Alert Processor

This project is an Azure Function App in Python for processing Meltwater email alerts, extracting metadata, scraping articles, and handling fallback scenarios with Microsoft Graph email notifications.

## Features
- **HTTP-triggered route:**
  - `POST /api/parse-email`: Parses the incoming email HTML and performs the full pipeline of scraping, filtering and emailing.

- **Shared utilities:**
  - `parser_utils.py`: Extracts fields and calls the Playwright scraper service.
  - `gpt_stub.py`: Placeholder GPT filter and relevance checks.
  - `graph_client.py`: Microsoft Graph email helpers.

## Project Structure
```
EmailParserFunctionApp/
├── parse_email/
│   ├── __init__.py           # Main entrypoint
│   ├── function.json         # HTTP trigger for /parse-email
├── shared/
│   ├── parser_utils.py       # extract_fields() + call_playwright_scraper()
│   ├── gpt_stub.py           # placeholder GPT checks
│   ├── graph_client.py       # Microsoft Graph helpers
├── requirements.txt
├── host.json
└── local.settings.json
```

## Environment Variables
Set these in `local.settings.json` or your Azure Function App configuration:
- `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`: For Microsoft Graph API authentication
- `SENDER_EMAIL`, `SLT_RECIPIENT_EMAIL`: Email addresses for sending/receiving
- `PLAYWRIGHT_API_URL`: Endpoint for Playwright scraping

## Requirements
- Python 3.8+
- Azure Functions Core Tools
- Dependencies: `azure-functions`, `requests`, `beautifulsoup4`

## Usage
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the function app:
   ```
   func start
   ```
3. Call the HTTP endpoint (e.g., using curl or Postman):
   - `POST /api/parse-email`

## Notes
- The pipeline runs entirely inside the `parse-email` function.
- Fallback emails are sent with normal importance when scraping or filtering fails.

---
