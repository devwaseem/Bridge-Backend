from django.db import models

from bridge.models import CandidateVideo
from bridge.utils.basemodel import BaseModel


class ShortlistGroup(BaseModel):
    name = models.CharField(max_length=255)
    videos = models.ManyToManyField(
        CandidateVideo, related_name="shortlist_groups", through="ShortlistGroupVideo"
    )

    class Meta:
        db_table = "shortlist_group"


class ShortlistGroupVideo(BaseModel):
    shortlist_group = models.ForeignKey(ShortlistGroup, on_delete=models.CASCADE)
    video = models.ForeignKey(CandidateVideo, on_delete=models.CASCADE)

    class Meta:
        db_table = "shortlist_group_video_map"
