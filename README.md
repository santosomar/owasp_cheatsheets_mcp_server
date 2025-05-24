# OWASP Cheat Sheet MCP Server

A minimal Model Context Protocol (MCP) compatible server providing the OWASP Cheat Sheets.

The server uses [FastAPI](https://fastapi.tiangolo.com/) to expose a simple HTTP API that returns the contents of the cheat sheets from the [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries).

## Prerequisites

- Python 3.8 or newer
- Git (for cloning the cheat sheet repository on first run)

## Usage

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. *(Optional)* Set `CHEATSHEETS_DIR` if you already have a local copy of the cheat sheets:
   ```bash
   export CHEATSHEETS_DIR=/path/to/CheatSheetSeries/cheatsheets
   ```
3. Run the server with `uvicorn`:
   ```bash
   uvicorn server.app:app --reload
   ```
4. If `CHEATSHEETS_DIR` is not set the server will clone the cheat sheet repository on first start (requires network access).

### Endpoints

- `GET /health` – Basic health check.
- `GET /cheatsheets` – List available cheat sheet files.
- `GET /cheatsheets/{name}` – Retrieve a specific cheat sheet.
- `GET /search?q=term` – Search cheat sheets for a term and return matching file names.

### Running in production

Use `uvicorn` with explicit host and port when deploying:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

For a real deployment consider a process manager such as `systemd` or running behind a reverse proxy.

### Contributing

Pull requests are welcome. Tests can be added under a `tests/` directory using [pytest](https://docs.pytest.org/).

This implementation is a simplified example of an MCP server and may not cover the entire specification.
