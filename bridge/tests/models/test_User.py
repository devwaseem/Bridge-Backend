import pytest
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.core.exceptions import ValidationError
from faker import Faker
from mixer.backend.django import mixer

from bridge.models import User
from bridge.tokens import EmailVerificationToken

pytestmark = pytest.mark.django_db
faker = Faker()


class TestModelUser:
    @pytest.mark.unit
    def test_User_db_table_is_user(self):
        assert User._meta.db_table == "user"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "non_superadmin_role", [User.Role.CANDIDATE, User.Role.RECRUITER]
    )
    def test_is_superuser_is_yes_only_when_role_is_superadmin(
        self, non_superadmin_role
    ):
        superadmin_user = mixer.blend(User, role=User.Role.SUPER_ADMIN)
        non_superadmin_user = mixer.blend(User, role=non_superadmin_role)

        assert non_superadmin_user.is_superuser is False
        assert non_superadmin_user.is_staff is False
        assert superadmin_user.is_superuser is True
        assert superadmin_user.is_staff is True

    @pytest.mark.unit
    def test_fn_create_superuser_creates_superuser(self):
        expected_role = User.Role.SUPER_ADMIN
        user = User.objects.create_superuser(
            email=faker.email(), password=faker.password()
        )

        assert user.id is not None
        assert expected_role == user.role
        assert user.is_superuser is True

    @pytest.mark.unit
    @pytest.mark.parametrize("role", User.Role.values)
    def test_fn_create_user_creates_user(self, role):
        expected_email = faker.email()
        expected_role = role
        user = User.objects.create_user(
            email=expected_email, password=faker.password(), role=expected_role
        )

        assert user.id is not None
        assert expected_email == user.email
        assert expected_role == user.role

    @pytest.mark.unit
    def test_fn_create_user_raises_exception_when_role_is_not_valid(self):
        with pytest.raises(ValueError) as exc:
            User.objects.create_user(
                email=faker.email(), password=faker.password(), role=faker.password()
            )
            assert "Invalid role" in str(exc.value)

    @pytest.mark.unit
    def test_fn_create_user_raises_exception_when_role_is_None(self):
        with pytest.raises(ValueError) as exc:
            User.objects.create_user(
                email=faker.email(), password=faker.password(), role=None
            )
            assert "User must have an role" in str(exc.value)

    @pytest.mark.unit
    def test_fn_create_user_raises_exception_when_email_is_None(self):
        with pytest.raises(ValueError) as exc:
            User.objects.create_user(
                email=None, password=faker.password(), role=User.Role.CANDIDATE
            )
            assert "User must have an email address" in str(exc.value)

    @pytest.mark.unit
    def test_fn_create_user_raises_exception_when_password_is_None(self):
        with pytest.raises(ValueError) as exc:
            User.objects.create_user(
                email=faker.email(), password=None, role=User.Role.CANDIDATE
            )
            assert "User must have an password" in str(exc.value)

    @pytest.mark.unit
    def test_fn_create_user_raises_exception_when_email_is_not_valid(self):
        with pytest.raises(ValidationError) as exc:
            User.objects.create_user(
                email=faker.word(),
                password=faker.password(),
                role=mixer.RANDOM(User.Role.values),
            )
            assert "Invalid email address" in str(exc.value), "Error did not raised"

    @pytest.mark.unit
    def test_fn_send_send_confirmation_email_sends_email_correctly_if_user_is_not_verified(
        self,
    ):
        user = mixer.blend(User, is_email_verified=False)
        user.send_confirmation_email()
        assert len(mail.outbox) == 1
        assert len(mail.outbox[0].to) == 1
        assert user.email == mail.outbox[0].to[0]
        assert "Confirm your email address" == mail.outbox[0].subject
        assert mail.outbox[0].body.find(f"{settings.FRONTEND_URL}/verify-email") != -1

    @pytest.mark.unit
    def test_fn_send_send_confirmation_email_does_not_send_email_if_user_is_verified_already(
        self,
    ):
        user = mixer.blend(User, is_email_verified=True)
        user.send_confirmation_email()
        assert len(mail.outbox) == 0

    @pytest.mark.unit
    def test_fn_confirm_email_verifies_user_with_valid_token(self):
        # Given
        user = mixer.blend(User, is_email_verified=False)
        token = EmailVerificationToken().make_token(user)

        # When
        verified = user.confirm_email(token)

        # Then
        assert verified
        assert user.is_email_verified

    @pytest.mark.unit
    def test_fn_confirm_email_does_not_verifies_user_with_expired_token(self):
        # Given
        user = mixer.blend(User, is_email_verified=False)
        # When
        verified = user.confirm_email("invalid_token")

        # Then
        assert not verified
        assert not user.is_email_verified

    @pytest.mark.unit
    def test_fn_send_password_reset_email_sends_email_correctly(self):
        user = mixer.blend(User)
        user.send_password_reset_email()
        assert len(mail.outbox) == 1
        assert len(mail.outbox[0].to) == 1
        assert user.email == mail.outbox[0].to[0]
        assert "Reset your password" == mail.outbox[0].subject
        assert mail.outbox[0].body.find(f"{settings.FRONTEND_URL}/reset-password") != -1

    @pytest.mark.unit
    def test_fn_reset_password_using_token_resets_password_correctly_with_valid_token(
        self,
    ):
        user = mixer.blend(User)
        new_password = faker.password()
        token = PasswordResetTokenGenerator().make_token(user)
        reset_done = user.reset_password_using_token(token, new_password)
        assert reset_done
        assert user.check_password(new_password)

    @pytest.mark.unit
    def test_fn_reset_password_using_token_does_not_resets_password_with_invalid_token(
        self,
    ):
        user = mixer.blend(User)
        new_password = faker.password()
        reset_done = user.reset_password_using_token("invalid_token", new_password)
        assert not reset_done
        assert not user.check_password(new_password)

    @pytest.mark.unit
    def test_fn_reset_password_using_current_password_resets_password_with_valid_current_password(
        self,
    ):
        user = mixer.blend(User)
        current_password = faker.password()
        user.set_password(current_password)
        user.save()

        new_password = faker.password()
        reset_done = user.reset_password_using_current_password(
            current_password, new_password
        )
        assert reset_done
        assert user.check_password(new_password)

    @pytest.mark.unit
    def test_fn_reset_password_using_current_password_resets_password_with_wrong_current_password(
        self,
    ):
        user = mixer.blend(User)

        new_password = faker.password()
        reset_done = user.reset_password_using_current_password(
            faker.password(), new_password
        )
        assert not reset_done
        assert not user.check_password(new_password)
