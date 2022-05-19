import pytest

from bridge.models import CandidateSkill

pytestmark = pytest.mark.django_db


class TestCandidateSkill:
    @pytest.mark.unit
    def test_candidate_skill_model_has_custom_db_table_name(self):
        assert CandidateSkill._meta.db_table == "candidate_skill"
