import sys
import importlib
from fastapi.testclient import TestClient
import pytest

@pytest.fixture()
def client(tmp_path, monkeypatch):
    cheat_dir = tmp_path / "cheats"
    cheat_dir.mkdir()
    (cheat_dir / "sheet1.md").write_text("Hello world")
    (cheat_dir / "sheet2.md").write_text("Another sheet")
    monkeypatch.setenv("CHEATSHEETS_DIR", str(cheat_dir))
    if "server.app" in sys.modules:
        del sys.modules["server.app"]
    module = importlib.import_module("server.app")
    with TestClient(module.app) as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_cheatsheets(client):
    resp = client.get("/cheatsheets")
    assert resp.status_code == 200
    assert set(resp.json()["cheatsheets"]) == {"sheet1.md", "sheet2.md"}


def test_get_cheatsheet(client):
    resp = client.get("/cheatsheets/sheet1.md")
    assert resp.status_code == 200
    assert "Hello world" in resp.text


def test_get_cheatsheet_not_found(client):
    resp = client.get("/cheatsheets/missing.md")
    assert resp.status_code == 404


def test_search(client):
    resp = client.get("/search", params={"q": "world"})
    assert resp.status_code == 200
    assert resp.json()["results"] == ["sheet1.md"]
