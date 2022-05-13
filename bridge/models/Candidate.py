from typing import Optional

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .CandidateDepartment import CandidateDepartment
from .CandidateSkill import CandidateSkill
from .CandidateSpecialization import CandidateSpecialization
from .User import User


class CandidateManager(models.Manager):
    @transaction.atomic
    def create_candidate(self, email: str, password: str) -> "Candidate":

        user = User.objects.create_user(
            email=email, password=password, role=User.Role.CANDIDATE
        )

        candidate = self.model(
            user=user,
        )

        candidate.save(using=self._db)

        return candidate


class Candidate(models.Model):
    objects = CandidateManager()

    class Gender(models.TextChoices):
        MALE = "MALE", _("Male")
        FEMALE = "FEMALE", _("Female")
        NON_BINARY = "NON_BINARY", _("Non binary")
        PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", _("Prefer not to say")

    user = models.OneToOneField("User", primary_key=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=Gender.choices)
    specialization = models.ForeignKey(
        CandidateSpecialization, on_delete=models.PROTECT, null=True
    )
    skills = models.ManyToManyField(CandidateSkill)
    department = models.ForeignKey(
        CandidateDepartment, on_delete=models.PROTECT, null=True
    )

    @property
    def industry(self) -> str:
        return self.department.industry

    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            return timezone.now().year - self.date_of_birth.year
        return None

    class Meta:
        db_table = "candidate"
