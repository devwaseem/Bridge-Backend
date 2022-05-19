import pytest

from bridge.models import CandidateIndustry

pytestmark = pytest.mark.django_db


class TestCandidateIndustry:
    @pytest.mark.unit
    def test_candidate_industry_model_has_custom_db_table_name(self):
        assert CandidateIndustry._meta.db_table == "candidate_industry"
