# Azure Function App: Meltwater Email Alert Processor

This project is an Azure Function App in Python for processing Meltwater email alerts, extracting metadata, scraping articles, and handling fallback scenarios with Microsoft Graph email notifications.

## Features
- **HTTP-triggered routes:**
  1. `POST /parse-email`: Extracts metadata from HTML and scrapes the article using Playwright. Returns fallback JSON if scraping fails.
  2. `POST /handle-playwright-failure`: Sends a fallback email via Microsoft Graph if scraping fails.
  3. `POST /handle-gpt-filter-failure`: Sends a fallback email if GPT filter blocks the content.
  4. `POST /handle-relevance-failure`: Sends article as non-SLT-relevant with normal importance.
  5. `POST /final-delivery`: Sends the final article email with importance based on content.

- **Shared utilities:**
  - `parser_utils.py`: Extracts fields from HTML and calls the Playwright scraper API.
  - `graph_client.py`: Handles Microsoft Graph authentication and email sending.

## Project Structure
```
EmailParserFunctionApp/
├── parse_email/
│   ├── __init__.py           # Contains main() + all 5 routes
│   ├── function.json         # HTTP trigger for /parse-email
├── shared/
│   ├── parser_utils.py       # extract_fields() + call_playwright_scraper()
│   ├── graph_client.py       # get_graph_token() + send_email()
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
3. Call the HTTP endpoints (e.g., using curl or Postman):
   - `POST /api/parse-email`
   - `POST /api/handle-playwright-failure`
   - `POST /api/handle-gpt-filter-failure`
   - `POST /api/handle-relevance-failure`
   - `POST /api/final-delivery`

## Notes
- Each route is implemented so it can be split into a separate Azure Function if needed.
- Email importance is set to "high" if `campaignName` or `articleTitle` contains "SLT" (case-insensitive), otherwise "normal".
- On scraping/filter/relevance failures, fallback emails are sent with normal importance.

---
