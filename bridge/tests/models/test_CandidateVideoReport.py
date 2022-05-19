import pytest

from bridge.models import CandidateVideoReport

pytestmark = pytest.mark.django_db


class TestCandidateVideoReport:
    @pytest.mark.unit
    def test_candidate_video_report_model_has_custom_db_table_name(self):
        assert CandidateVideoReport._meta.db_table == "candidate_video_report"
