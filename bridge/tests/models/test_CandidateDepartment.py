import pytest

from bridge.models import CandidateDepartment

pytestmark = pytest.mark.django_db


class TestCandidateDepartment:
    @pytest.mark.unit
    def test_candidate_department_model_has_custom_db_table_name(self):
        assert CandidateDepartment._meta.db_table == "candidate_department"
