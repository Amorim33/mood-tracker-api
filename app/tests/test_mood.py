import os

from fastapi import status
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.main import app

client = TestClient(app)


# it returns the happy mood for the test audio file
@freeze_time("2004-03-15 00:00:01")
def test_happy_mood():
    with open(os.path.abspath("assets/happy.wav"), "rb") as file:
        response = client.post(
            "/api/v1/mood",
            files={"file": ("happy", file, "audio/wav")},
        )

    data = response.json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert data == {
        "mood": "Happy",
        "date": "2004-03-15",
    }


# it returns the mood for the test webm file
@freeze_time("2004-03-15 00:00:01")
def test_webm_mood():
    with open(os.path.abspath("assets/input.webm"), "rb") as file:
        response = client.post(
            "/api/v2/mood",
            files={"file": ("input", file, "audio/webm")},
        )

    data = response.json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert data == {
        "mood": "Happy",
        "date": "2004-03-15",
    }
