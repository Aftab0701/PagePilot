"""
Unit and integration tests for PagePilot FastAPI WebUI server.
"""

import pytest
from fastapi.testclient import TestClient
from pagepilot.webui.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "pagepilot"
    assert "version" in data


def test_root_index_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "PagePilot" in response.text
    assert "tokens.css" in response.text
    assert "components.css" in response.text
    assert "app.js" in response.text


def test_static_tokens_css(client):
    response = client.get("/static/css/tokens.css")
    assert response.status_code == 200
    assert "--bg:" in response.text
    assert "--ac:" in response.text


def test_static_components_css(client):
    response = client.get("/static/css/components.css")
    assert response.status_code == 200
    assert ".topbar" in response.text
    assert ".status" in response.text
    assert ".view" in response.text


def test_static_app_js(client):
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert "PagePilot" in response.text
    assert "runSimulated" in response.text


def test_websocket_agent_communication(client):
    with client.websocket_connect("/ws/agent") as websocket:
        # Send start message
        websocket.send_json({
            "action": "start",
            "task": "Test navigation to python.org",
            "settings": {
                "provider": "google",
                "model": "gemini-2.5-flash",
                "maxSteps": 2
            }
        })
        
        # We expect at least one step update
        data = websocket.receive_json()
        assert "type" in data
        assert data["type"] in ["step", "done", "error"]
        
        # Test stop message
        websocket.send_json({"action": "stop"})
        stop_resp = websocket.receive_json()
        assert stop_resp["type"] == "error"
        assert "stopped" in stop_resp["message"].lower()
