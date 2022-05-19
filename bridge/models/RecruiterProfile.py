from django.db import models

from bridge.models.Company import Company
from bridge.models.User import User
from bridge.utils.basemodel import BaseModel


class RecruiterProfile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="recruiter_profile"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "recruiter_profile"
