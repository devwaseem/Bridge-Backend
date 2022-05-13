import pytest
from django.core.exceptions import ValidationError
from faker import Faker
from mixer.backend.django import mixer

from bridge.models import User

pytestmark = pytest.mark.django_db
faker = Faker()


class TestModelUser:
    @pytest.mark.unit
    def test_db_table_is_user(self):
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
