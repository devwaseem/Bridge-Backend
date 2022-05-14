from django.urls import path

from .api.views.candidate.auth import CandidateLoginAPIView, CandidateSignupAPIView

app_name = "bridge"

# Public urls
# ------------------------------------------------------------------------------
urlpatterns = []

# Private:Candidate urls
# ------------------------------------------------------------------------------

urlpatterns += [
    path("candidate/login", CandidateLoginAPIView.as_view(), name="candidate_login"),
    path("candidate/signup", CandidateSignupAPIView.as_view(), name="candidate_signup"),
]

# Private:Recruiter urls
# ------------------------------------------------------------------------------

urlpatterns += []
