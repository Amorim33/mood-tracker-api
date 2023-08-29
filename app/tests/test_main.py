from fastapi.testclient import TestClient

from app.__version__ import __version__
from app.main import app

client = TestClient(app)


# it gets the main route
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Mood Tracker API is running! 🚀",
        "version": __version__,
    }
