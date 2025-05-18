from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pathlib import Path
import subprocess
import os

app = FastAPI(title="OWASP Cheat Sheets MCP Server")

CHEATSHEETS_DIR = Path(os.getenv("CHEATSHEETS_DIR", "data/CheatSheetSeries/cheatsheets"))

@app.on_event("startup")
def startup_event():
    """Ensure cheat sheets are present. Clone repo if necessary."""
    if not CHEATSHEETS_DIR.exists():
        repo_url = "https://github.com/OWASP/CheatSheetSeries.git"
        dest = CHEATSHEETS_DIR.parent.parent
        dest.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run([
                "git", "clone", "--depth", "1", repo_url, str(dest)
            ], check=True)
        except Exception as exc:
            logging.error(f"Failed to clone cheat sheet repo: {exc}")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cheatsheets")
def list_cheatsheets():
    if not CHEATSHEETS_DIR.exists():
        raise HTTPException(status_code=500, detail="Cheat sheets directory not found")
    files = [f.name for f in CHEATSHEETS_DIR.glob("*.md")]
    return {"cheatsheets": files}

@app.get("/cheatsheets/{name}", response_class=PlainTextResponse)
def get_cheatsheet(name: str):
    try:
        # Resolve the full path and ensure it is within CHEATSHEETS_DIR
        file_path = (CHEATSHEETS_DIR / name).resolve()
        if not file_path.is_file() or not str(file_path).startswith(str(CHEATSHEETS_DIR)):
            raise HTTPException(status_code=404, detail="Cheat sheet not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid cheat sheet name")
    return file_path.read_text()

@app.get("/search")
def search_cheatsheets(q: str):
    if not CHEATSHEETS_DIR.exists():
        raise HTTPException(status_code=500, detail="Cheat sheets directory not found")
    result = []
    for path in CHEATSHEETS_DIR.glob("*.md"):
        text = path.read_text(errors="ignore")
        if q.lower() in text.lower():
            result.append(path.name)
    return {"results": result}
