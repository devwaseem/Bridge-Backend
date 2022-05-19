import pytest

from bridge.models import Company

pytestmark = pytest.mark.django_db


class TestCompany:
    @pytest.mark.unit
    def test_company_model_has_custom_db_table_name(self):
        assert Company._meta.db_table == "company"
