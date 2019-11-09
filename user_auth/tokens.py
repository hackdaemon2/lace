from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AuthTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type( user.pk) + six.text_type(timestamp) + six.text_type(user.email)
        
password_reset_token = AuthTokenGenerator()
verify_email_token = AuthTokenGenerator()