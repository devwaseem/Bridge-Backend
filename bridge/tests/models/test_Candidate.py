import pytest
from django.utils import timezone
from faker import Faker
from mixer.backend.django import mixer

from bridge.models import Candidate, User

pytestmark = pytest.mark.django_db
faker = Faker()


class TestModelCandidate:
    @pytest.mark.unit
    def test_Candidate_db_table_is_user(self):
        assert Candidate._meta.db_table == "candidate"

    @pytest.mark.unit
    def test_fn_create_candidate_creates_candidate_with_user_successfully(self):
        expected_email = faker.email()
        candidate = Candidate.objects.create_candidate(
            email=expected_email,
            password=faker.password(),
        )

        assert candidate.pk is not None
        assert candidate.user.pk is not None
        assert candidate.user.email == expected_email
        assert candidate.user.role == User.Role.CANDIDATE

    @pytest.mark.unit
    def test_industry_is_departments_industry(self):
        candidate = mixer.blend(Candidate)
        assert candidate.industry == candidate.department.industry

    @pytest.mark.unit
    @pytest.mark.parametrize("dob", [faker.date_of_birth() for _ in range(10)])
    def test_age_is_calculated_correctly(self, dob):
        candidate = mixer.blend(Candidate, date_of_birth=dob)
        assert candidate.age == timezone.now().year - candidate.date_of_birth.year

    @pytest.mark.unit
    def test_age_is_none_when_dob_is_not_set(self):
        candidate = mixer.blend(Candidate, date_of_birth=None)
        assert candidate.age is None

    @pytest.mark.unit
    def test_when_new_candidate_created_signup_step_is_1(self):
        candidate = Candidate.objects.create_candidate(
            email=faker.email(),
            password=faker.password(),
        )
        assert candidate.user.signup_step == 1
