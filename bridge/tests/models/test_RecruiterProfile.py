import pytest

from bridge.models import RecruiterProfile

pytestmark = pytest.mark.django_db


class TestRecruiterProfile:
    @pytest.mark.unit
    def test_recruiter_profile_model_has_custom_db_table_name(self):
        assert RecruiterProfile._meta.db_table == "recruiter_profile"
