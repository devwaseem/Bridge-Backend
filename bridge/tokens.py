from django.contrib.auth.tokens import default_token_generator


class EmailVerificationToken(default_token_generator):
    def _make_hash_value(self, user, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        return f"{user.pk}{timestamp}{email}{user.email_verified}"
