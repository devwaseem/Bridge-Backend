from django.db import models

from bridge.models.CandidateIndustry import CandidateIndustry
from bridge.utils.basemodel import BaseModel


class CandidateDepartment(BaseModel):
    name = models.CharField(max_length=255)
    industry = models.ForeignKey(CandidateIndustry, on_delete=models.CASCADE)

    class Meta:
        db_table = "candidate_department"
