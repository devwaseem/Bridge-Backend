import pytest

from bridge.models import ShortlistGroup

pytestmark = pytest.mark.django_db


class TestShortlistGroup:
    @pytest.mark.unit
    def test_shortlist_group_model_has_custom_db_table_name(self):
        assert ShortlistGroup._meta.db_table == "shortlist_group"
