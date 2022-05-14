import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, role, **extra_fields) -> "User":
        if not email:
            raise ValueError(_("User must have an email address"))

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Invalid email address"))

        if not password:
            raise ValueError(_("User must have an password"))

        if not role:
            raise ValueError(_("User must have an role"))

        if role not in User.Role:
            raise ValueError(_("Invalid role"))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.role = role
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        user = self.create_user(
            email=email, password=password, role=User.Role.SUPER_ADMIN, **extra_fields
        )
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Default custom user model for Bridge.
    """

    # Default overrides
    # -----------------------------------------------------------------------------
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPERADMIN", _("Super Admin")
        CANDIDATE = "CANDIDATE", _("Candidate")
        RECRUITER = "RECRUITER", _("Recruiter")

    #  Manager
    # -----------------------------------------------------------------------------
    objects = UserManager()

    # Fields
    # -----------------------------------------------------------------------------
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    date_joined = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    signup_step = models.PositiveSmallIntegerField(default=1)

    email = models.EmailField(unique=True, db_index=True)
    fullname = models.CharField(_("Fullname"), blank=True, max_length=255)
    role = models.CharField(
        max_length=100, choices=Role.choices, verbose_name=_("Role")
    )
    username = None
    groups = None
    user_permissions = None

    # TODO: Add Avatar with custom upload path and size checks
    # avatar = models.ImageField(upload_to="avatars", blank=True)

    @property
    def is_superuser(self) -> bool:
        return self.role == User.Role.SUPER_ADMIN

    @property
    def is_staff(self) -> bool:
        return self.role == User.Role.SUPER_ADMIN

    class Meta:
        db_table = "user"
