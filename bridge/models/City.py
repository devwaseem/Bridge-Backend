from django.db import models

from bridge.models.Country import Country
from bridge.utils.basemodel import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        db_table = "city"
