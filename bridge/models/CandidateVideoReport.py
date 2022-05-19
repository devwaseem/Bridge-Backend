from django.db import models

from bridge.models.CandidateVideo import CandidateVideo
from bridge.models.User import User
from bridge.utils.basemodel import BaseModel


class CandidateVideoReport(BaseModel):
    video = models.ForeignKey(CandidateVideo, on_delete=models.CASCADE)
    report_text = models.TextField(blank=True, null=True, max_length=2000)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "candidate_video_report"
        unique_together = ("video", "reported_by")
