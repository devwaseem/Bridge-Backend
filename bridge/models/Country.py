from django.db import models

from bridge.utils.basemodel import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "country"
