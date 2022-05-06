import pytest
from django.urls import reverse
from mixer.backend.django import mixer

from bridge.users.models import User

pytestmark = pytest.mark.django_db


def test_swagger_accessible_by_admin(admin_client):
    url = reverse("api-docs")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_swagger_ui_not_accessible_by_normal_user(client):
    url = reverse("api-docs")
    user = mixer.blend(User, role=(User.Role.CANDIDATE, User.Role.RECRUITER))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


def test_swagger_ui_not_accessible_by_public(client):
    url = reverse("api-docs")
    response = client.get(url)
    assert response.status_code == 401


def test_api_schema_generated_successfully(admin_client):
    url = reverse("api-schema")
    response = admin_client.get(url)
    assert response.status_code == 200
