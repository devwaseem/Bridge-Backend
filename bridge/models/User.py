import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from bridge.tokens import EmailVerificationToken


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
        user.verify_email()
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Default custom user model for Bridge.
    """

    class Meta:
        db_table = "user"

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
    is_email_verified = models.BooleanField(default=False)

    username = None
    groups = None
    user_permissions = None

    # TODO: Add Avatar with custom upload path and size checks
    # avatar = models.ImageField(upload_to="avatars", blank=True)

    @property
    def is_superuser(self) -> bool:
        return self.role == User.Role.SUPER_ADMIN

    @property
    def is_candidate(self) -> bool:
        return self.role == User.Role.CANDIDATE

    @property
    def is_recruiter(self) -> bool:
        return self.role == User.Role.RECRUITER

    @property
    def is_staff(self) -> bool:
        return self.role == User.Role.SUPER_ADMIN

    @property
    def encoded_uid(self) -> str:
        """
        Return base64 encoded uid
        """
        return urlsafe_base64_encode(force_bytes(self.id))

    def send_confirmation_email(self):
        if self.is_email_verified:
            return

        uid = self.encoded_uid
        token = EmailVerificationToken().make_token(self)
        reset_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"

        subject = "Confirm your email address"
        html_message = render_to_string(
            "emails/auth/confirmation_email.html",
            {
                "email": self.email,
                "reset_link": reset_link,
            },
        )
        text_message = strip_tags(html_message)
        mail = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            to=[self.email],
        )
        mail.attach_alternative(html_message, "text/html")
        mail.send()

    def verify_email(self):
        self.is_email_verified = True
        self.save()

    def confirm_email(self, token: str) -> bool:
        if EmailVerificationToken().check_token(user=self, token=token):
            self.verify_email()
            return True
        return False

    def send_password_reset_email(self):
        subject = "Reset your password"
        token = PasswordResetTokenGenerator().make_token(self)
        reset_link = (
            f"{settings.FRONTEND_URL}/reset-password/{self.encoded_uid}/{token}"
        )
        html_message = render_to_string(
            "emails/auth/password_reset.html",
            {
                "reset_link": reset_link,
            },
        )
        text_message = strip_tags(html_message)
        mail = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            to=[self.email],
        )
        mail.attach_alternative(html_message, "text/html")
        mail.send()

    def reset_password_using_token(self, token: str, new_password: str) -> bool:
        if PasswordResetTokenGenerator().check_token(user=self, token=token):
            self.set_password(new_password)
            self.save(update_fields=["password"])
            return True
        return False

    def reset_password_using_current_password(
        self, current_password: str, new_password: str
    ) -> bool:
        if self.check_password(current_password):
            self.set_password(new_password)
            self.save(update_fields=["password"])
            return True
        return False
