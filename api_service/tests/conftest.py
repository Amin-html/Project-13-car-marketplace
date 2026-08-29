import os
import sys
import django
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, "/django_core")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def create_user(db):
    from accounts.models import User

    def _create(username="testuser", role="buyer", password="testpass123"):
        user = User.objects.create_user(username=username, password=password, role=role)
        return user
    return _create

@pytest.fixture
def auth_headers(create_user):
    from app.core.security import create_access_token

    def _headers(role="buyer", username="testuser"):
        user = create_user(username=username, role=role)
        token = create_access_token(user_id=user.id, role=user.role)
        return {"Authorization": f"Bearer {token}"}, user
    return _headers