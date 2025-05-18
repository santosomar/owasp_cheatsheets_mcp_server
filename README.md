# owasp_cheatsheets_mcp_server

A minimal Model Context Protocol (MCP) compatible server providing the OWASP Cheat Sheets.

The server uses [FastAPI](https://fastapi.tiangolo.com/) to expose a simple HTTP API that returns the contents of the cheat sheets from the [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries).

## Usage

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server with `uvicorn`:
   ```bash
   uvicorn server.app:app --reload
   ```
3. The server will clone the cheat sheet repository on first start (requires network access) unless the environment variable `CHEATSHEETS_DIR` points to an existing directory containing the Markdown files.

### Endpoints

- `GET /health` – Basic health check.
- `GET /cheatsheets` – List available cheat sheet files.
- `GET /cheatsheets/{name}` – Retrieve a specific cheat sheet.
- `GET /search?q=term` – Search cheat sheets for a term and return matching file names.

This implementation is a simplified example of an MCP server and may not cover the entire specification.
