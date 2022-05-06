from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from bridge.utils.basemodel import BaseModel

from .User import User


class CandidateSpecialization(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Candidate Specialization"
        verbose_name_plural = "Candidate Specializations"


class CandidateSkill(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Candidate Skill"
        verbose_name_plural = "Candidate Skills"


class CandidateManager(models.Manager):
    @transaction.atomic
    def create_candidate(self, **kwargs):
        required_fields = ["email", "password"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(_(f"Candidate must have an {field}"))

        user = User(
            email=self.normalize_email(kwargs["email"]),
        )
        user.set_password(kwargs["password"])
        user.role = User.Role.CANDIDATE
        user.save(using=self._db)

        candidate = self.model(
            user=user,
        )

        candidate.save()

        return user


class Candidate(models.Model):
    objects = CandidateManager()

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    specialization = models.ForeignKey(
        CandidateSpecialization, on_delete=models.PROTECT, null=True
    )
    skills = models.ManyToManyField(CandidateSkill)
