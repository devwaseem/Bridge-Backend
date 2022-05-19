from django.db import models

from bridge.utils.basemodel import BaseModel


class CandidateVideo(BaseModel):
    candidate = models.ForeignKey(
        "bridge.CandidateProfile", on_delete=models.CASCADE, null=False, blank=False
    )
    thumbnail = models.ImageField(
        upload_to="candidate_video/thumbnail/", blank=False, null=False
    )
    video = models.FileField(upload_to="videos/", null=False, blank=False)
    transcript = models.TextField(null=True, blank=False, max_length=4000)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        db_table = "candidate_video"
