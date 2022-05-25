from django.urls import path

from .api.views.auth import (
    ConfirmEmailApiView,
    IsAuthenticatedApiView,
    PasswordChangeApiView,
    PasswordResetApiView,
    PasswordResetInitiateApiView,
)
from .api.views.candidate.auth import CandidateLoginAPIView, CandidateSignupAPIView
from .api.views.recruiter.auth import RecruiterLoginAPIView

app_name = "bridge"

# Public urls
# ------------------------------------------------------------------------------
urlpatterns = [
    path(
        "auth/confirm-email/<uidb64>/<token>",
        ConfirmEmailApiView.as_view(),
        name="confirm_email",
    ),
    path(
        "auth/reset-password-initiate/",
        PasswordResetInitiateApiView.as_view(),
        name="reset_password_initiate",
    ),
    path(
        "auth/reset-password/<uidb64>/<token>",
        PasswordResetApiView.as_view(),
        name="reset_password",
    ),
    path(
        "auth/change-password/",
        PasswordChangeApiView.as_view(),
        name="change_password",
    ),
    path(
        "auth/is-authenticated/",
        IsAuthenticatedApiView.as_view(),
        name="is_authenticated",
    ),
]

# Private:CandidateProfile urls
# ------------------------------------------------------------------------------

urlpatterns += [
    path("candidate/login", CandidateLoginAPIView.as_view(), name="candidate_login"),
    path("candidate/signup", CandidateSignupAPIView.as_view(), name="candidate_signup"),
]

# Private:Recruiter urls
# ------------------------------------------------------------------------------

urlpatterns += [
    path("recruiter/login", RecruiterLoginAPIView.as_view(), name="recruiter_login"),
]
