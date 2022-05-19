import pytest

from bridge.models import City

pytestmark = pytest.mark.django_db


class TestCity:
    @pytest.mark.unit
    def test_city_model_has_custom_db_table_name(self):
        assert City._meta.db_table == "city"
