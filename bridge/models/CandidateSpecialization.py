from django.db import models

from bridge.utils.basemodel import BaseModel


class CandidateSpecialization(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Candidate Specialization"
        verbose_name_plural = "Candidate Specializations"
        db_table = "candidate_specialization"
