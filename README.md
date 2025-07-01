# Data Analyst Agent API

An API that uses LLMs to source, prepare, analyze, and visualize data.

## Features

- Accepts data analysis tasks via POST requests
- Handles web scraping and DuckDB queries
- Generates visualizations
- Returns results in JSON format

## Deployment

1. Set up Vercel account
2. Install Vercel CLI: `npm install -g vercel`
3. Deploy: `vercel`

## Environment Variables

- `LLM_API_BASE`: Base URL for LLM API (default: https://aiproxy.sanand.workers.dev/openai/)

## API Endpoint

`POST /api/` - Submit a data analysis task
`GET /health` - Health check