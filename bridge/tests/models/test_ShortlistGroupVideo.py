import pytest

from bridge.models import ShortlistGroupVideo

pytestmark = pytest.mark.django_db


class TestShortlistGroupVideo:
    @pytest.mark.unit
    def test_shortlist_group_video_model_has_custom_db_table_name(self):
        assert ShortlistGroupVideo._meta.db_table == "shortlist_group_video_map"
