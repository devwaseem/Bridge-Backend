import pytest

from bridge.models import Country

pytestmark = pytest.mark.django_db


class TestCountry:
    @pytest.mark.unit
    def test_country_model_has_custom_db_table_name(self):
        assert Country._meta.db_table == "country"
