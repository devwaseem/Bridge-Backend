from django.db import models

from bridge.utils.basemodel import BaseModel


class CandidateSkill(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Candidate Skill"
        verbose_name_plural = "Candidate Skills"
        db_table = "candidate_skill"
