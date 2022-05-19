import pytest

from bridge.models import CandidateVideo

pytestmark = pytest.mark.django_db


class TestCandidateVideo:
    @pytest.mark.unit
    def test_candidate_video_model_has_custom_db_table_name(self):
        assert CandidateVideo._meta.db_table == "candidate_video"
