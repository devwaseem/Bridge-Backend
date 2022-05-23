import pytest
from django.urls import reverse
from faker import Faker

from bridge.models import User

pytestmark = pytest.mark.django_db
faker = Faker("en_US")


class TestRecruiterApiAuth:

    # Login tests
    # --------------------------------------------------

    @pytest.mark.integration
    def test_recruiter_api_login_with_valid_credentials_for_recruiter_role_returns_auth_tokens(
        self, client
    ):
        recruiter_login_url = reverse("bridge:recruiter_login")
        email = faker.email()
        password = faker.password()
        User.objects.create_user(
            email=email, password=password, role=User.Role.RECRUITER
        )
        response = client.post(
            recruiter_login_url, {"email": email, "password": password}
        )

        assert response.status_code == 200
        assert "token" in response.data
        assert "signup_step" not in response.data

    @pytest.mark.integration
    def test_recruiter_api_login_with_valid_credentials_for_recruiter_role_with_inactive_account_returns_401_with_error(
        self, client
    ):
        candidate_login_url = reverse("bridge:recruiter_login")
        email = faker.email()
        password = faker.password()
        user = User.objects.create_user(
            email=email, password=password, role=User.Role.RECRUITER
        )
        user.is_active = False
        user.save()

        response = client.post(
            candidate_login_url, {"email": email, "password": password}
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Your account has been disabled"

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "role", [role for role in User.Role.values if role != User.Role.RECRUITER]
    )
    def test_recruiter_api_login_with_valid_credentials_for_non_recruiter_role_returns_401_with_error(
        self, client, role
    ):
        recruiter_login_url = reverse("bridge:recruiter_login")
        email = faker.email()
        password = faker.password()
        User.objects.create_user(email=email, password=password, role=role)
        response = client.post(
            recruiter_login_url, {"email": email, "password": password}
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Invalid credentials"

    @pytest.mark.integration
    @pytest.mark.parametrize("role", User.Role.values)
    def test_candidate_api_login_with_invalid_credentials_with_any_role_returns_401_with_error(
        self, client, role
    ):
        recruiter_login_url = reverse("bridge:recruiter_login")
        email = faker.email()
        password = faker.password()
        User.objects.create_user(email=email, password=password, role=role)
        response = client.post(
            recruiter_login_url, {"email": email, "password": faker.password()}
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Invalid credentials"
