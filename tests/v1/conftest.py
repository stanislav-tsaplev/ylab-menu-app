import pytest
from fastapi.testclient import TestClient

from app.main import app


LOCAL_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def client():
    cli = TestClient(app)
    yield cli
