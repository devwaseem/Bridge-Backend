import pytest

from bridge.models import CandidateSpecialization

pytestmark = pytest.mark.django_db


class TestCandidateSpecialization:
    @pytest.mark.unit
    def test_candidate_specialization_model_has_custom_db_table_name(self):
        assert CandidateSpecialization._meta.db_table == "candidate_specialization"
