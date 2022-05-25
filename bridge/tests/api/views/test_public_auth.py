import pytest
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_410_GONE,
)

from bridge.models import User
from bridge.tokens import EmailVerificationToken

pytestmark = pytest.mark.django_db


class TestPublicAuthActions:
    @pytest.mark.unit
    def test_confirm_email_api_verifies_user_with_correct_token(self, client):
        """
        Test that the confirm_email API verifies the user with the correct token
        """
        user = mixer.blend(User, is_email_verified=False)
        token = EmailVerificationToken().make_token(user)
        confirm_email_url = reverse(
            "bridge:confirm_email", kwargs={"token": token, "uidb64": user.encoded_uid}
        )
        response = client.get(confirm_email_url)
        user.refresh_from_db()

        assert response.status_code == HTTP_200_OK
        assert response.data["detail"] == "Your Email has been Verified."
        assert user.is_email_verified

    @pytest.mark.unit
    def test_confirm_email_api_does_not_verify_user_with_invalid_token(self, client):
        user = mixer.blend(User, is_email_verified=False)
        confirm_email_url = reverse(
            "bridge:confirm_email",
            kwargs={"token": "invalid_token", "uidb64": user.encoded_uid},
        )
        response = client.get(confirm_email_url)
        user.refresh_from_db()

        assert response.status_code == HTTP_410_GONE
        assert response.data["detail"] == "Link is invalid or expired."
        assert not user.is_email_verified

    @pytest.mark.unit
    def test_confirm_email_api_does_not_verify_a_non_existent_user(self, client):
        user = mixer.blend(User, is_email_verified=False)
        confirm_email_url = reverse(
            "bridge:confirm_email",
            kwargs={"token": "invalid_token", "uidb64": user.encoded_uid},
        )
        user.delete()
        response = client.get(confirm_email_url)

        assert response.status_code == HTTP_410_GONE
        assert response.data["detail"] == "Link is invalid or expired."

    @pytest.mark.integration
    def test_password_reset_initiate_api_sends_email_with_reset_link(self, client):
        user = mixer.blend(User)
        password_reset_url = reverse("bridge:reset_password_initiate")
        response = client.post(password_reset_url, {"email": user.email})
        assert response.status_code == HTTP_200_OK
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Reset your password"
        assert mail.outbox[0].body.find(f"{settings.FRONTEND_URL}/reset-password") != -1

    @pytest.mark.unit
    def test_password_reset_initiate_api_passes_but_does_not_send_email_with_reset_link_if_user_does_not_exists(
        self, client, faker
    ):
        password_reset_url = reverse("bridge:reset_password_initiate")
        response = client.post(password_reset_url, {"email": faker.email()})
        assert response.status_code == HTTP_200_OK
        assert len(mail.outbox) == 0

    @pytest.mark.unit
    def test_password_reset_api_resets_password_correctly_with_valid_token(
        self, client, faker
    ):
        user = mixer.blend(User)
        token = PasswordResetTokenGenerator().make_token(user)
        password_reset_url = reverse(
            "bridge:reset_password", kwargs={"token": token, "uidb64": user.encoded_uid}
        )
        new_password = faker.password()
        response = client.post(
            password_reset_url,
            {"new_password": new_password},
        )
        assert response.status_code == HTTP_200_OK
        assert response.data["detail"] == "Your password has been reset."
        user.refresh_from_db()
        assert user.check_password(new_password)

    @pytest.mark.unit
    def test_password_reset_api_does_not_resets_password_with_invalid_token(
        self, client, faker
    ):
        user = mixer.blend(User)
        token = "invalid_token"
        password_reset_url = reverse(
            "bridge:reset_password", kwargs={"token": token, "uidb64": user.encoded_uid}
        )
        new_password = faker.password()
        response = client.post(
            password_reset_url,
            {"new_password": new_password},
        )
        assert response.status_code == HTTP_410_GONE
        assert response.data["detail"] == "Link is invalid or expired."
        user.refresh_from_db()
        assert not user.check_password(new_password)

    @pytest.mark.unit
    def test_password_reset_api_does_not_resets_password_for_non_existent_user(
        self, client, faker
    ):
        user = mixer.blend(User)
        token = PasswordResetTokenGenerator().make_token(user)
        password_reset_url = reverse(
            "bridge:reset_password", kwargs={"token": token, "uidb64": user.encoded_uid}
        )
        new_password = faker.password()

        user.delete()

        response = client.post(
            password_reset_url,
            {"new_password": new_password},
        )
        assert response.status_code == HTTP_410_GONE
        assert response.data["detail"] == "Link is invalid or expired."

    @pytest.mark.unit
    def test_password_change_api_returns_401_for_unauthenticated_user(self, client):
        response = client.post(reverse("bridge:change_password"))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.unit
    def test_password_change_api_resets_password_with_correct_current_password(
        self, client, faker
    ):
        user = mixer.blend(User)
        current_password = faker.password()
        user.set_password(current_password)
        user.save()

        client.force_login(user)

        new_password = faker.password()
        password_change_url = reverse("bridge:change_password")
        response = client.post(
            password_change_url,
            {"current_password": current_password, "new_password": new_password},
        )

        assert response.status_code == HTTP_200_OK
        assert response.data["detail"] == "Your password has been changed."
        user.refresh_from_db()
        assert user.check_password(new_password)

    @pytest.mark.unit
    def test_password_change_api_does_not_resets_password_with_wrong_current_password(
        self, client, faker
    ):
        user = mixer.blend(User)
        current_password = faker.password()
        user.set_password(current_password)
        user.save()

        client.force_login(user)

        new_password = faker.password()
        password_change_url = reverse("bridge:change_password")
        client.force_login(user)
        response = client.post(
            password_change_url,
            {"current_password": faker.password(), "new_password": new_password},
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Your current password is incorrect."
        user.refresh_from_db()
        assert user.check_password(current_password)
