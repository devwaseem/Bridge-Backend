from typing import Any, Sequence

import factory.fuzzy
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from bridge.models import User


class UserFactory(DjangoModelFactory):

    fullname = Faker("name")
    email = Faker("email")
    role = factory.fuzzy.FuzzyChoice(User.Role.choices)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ["email"]
