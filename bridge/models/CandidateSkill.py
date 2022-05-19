from django.db import models

from bridge.utils.basemodel import BaseModel


class CandidateSkill(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "CandidateProfile Skill"
        verbose_name_plural = "CandidateProfile Skills"
        db_table = "candidate_skill"
