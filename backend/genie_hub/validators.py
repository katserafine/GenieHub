from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.conf import settings
from logging import getLogger

from .models import PreviousPassword

logger = getLogger("genie_hub.validators")

# Password validation settings
# - English uppercase character(s) (A through Z)
# - English lowercase character(s) (a through z)
# - Base 10 digits (0 through 9)
# - Non-alphabetic character(s) (for example, !, @, #, $)
# - Don't reuse previous five passwords

class UpperCaseCharactersValidator(object):
    def __init__(self, min_upper=1):
        self.min_upper = min_upper

    def validate(self, password, user=None):
        if sum(c.isupper() for c in password) < self.min_upper:
            raise ValidationError(
                _("Your password must contain at least %(min_upper)d uppercase character(s)."),
                code='not_enough_uppercase',
                params={'min_upper': self.min_upper},
            )

    def get_help_text(self):
        return _("Your password must contain at least %(min_upper)d uppercase character(s)." % {'min_upper': self.min_upper})


class LowerCaseCharactersValidator(object):
    def __init__(self, min_lower=1):
        self.min_lower = min_lower

    def validate(self, password, user=None):
        if sum(c.islower() for c in password) < self.min_lower:
            raise ValidationError(
                _("Your password must contain at least %(min_lower)d lowercase character(s)."),
                code='not_enough_lowercase',
                params={'min_lower': self.min_lower},
            )

    def get_help_text(self):
        return _("Your password must contain at least %(min_lower)d lowercase character(s)." % {'min_lower': self.min_lower})


class NumbersValidator(object):
    def __init__(self, min_numbers=1):
        self.min_numbers = min_numbers

    def validate(self, password, user=None):
        if sum(c.isdigit() for c in password) < self.min_numbers:
            raise ValidationError(
                _("Your password must contain at least %(min_numbers)d number(s)."),
                code='not_enough_numbers',
                params={'min_numbers': self.min_numbers},
            )

    def get_help_text(self):
        return _("Your password must contain at least %(min_numbers)d number(s)." % {'min_numbers': self.min_numbers})


class SpecialCharactersValidator(object):
    def __init__(self, min_characters=1):
        self.min_characters = min_characters
        self.allowed_characters = '~`!@#$%^&*()[]{}|;:<>,./?=+-_"\'\\'

    def validate(self, password, user=None):
        if sum(password.count(c) for c in self.allowed_characters) < self.min_characters:
            raise ValidationError(
                _("Your password must contain at least %(min_characters)d of the following special character(s) %(allowed_characters)s."),
                code='not_enough_numbers',
                params={'min_characters': self.min_characters, 'allowed_characters': self.allowed_characters},
            )

    def get_help_text(self):
        return _("Your password must contain at least %(min_characters)d of the following special character(s) %(allowed_characters)s." % {'min_characters': self.min_characters, 'allowed_characters': self.allowed_characters})


class PreviousPasswordsValidator(object):
    def __init__(self, history_length=5):
        self.history_length = history_length
        self.salt_factor = 9876

    def validate(self, password, user=None):
        if not user or not user.pk:
          return

        # Use the user PK as a hash for the purpose of password history
        # Not random, but will be different for every user.
        password_hash = make_password(password, str(user.pk * self.salt_factor))

        if PreviousPassword.objects.filter(django_user=user, password_hash=password_hash).exists():
            raise ValidationError(
                _("Your password must be different than the previous %(history_length)d passwords you have used."),
                code='previously_used',
                params={'history_length': self.history_length,},
            )

    # Hash the new password and stores it for future comparison,
    # then trim the history so we only have the last 5 (including the newest one)
    def password_changed(self, password, user=None):
        if not user or not user.pk:
          return

        new_password = PreviousPassword.objects.create(django_user=user, password_hash=make_password(password, str(user.pk * self.salt_factor)))

        previous_password_ids = PreviousPassword.objects.filter(django_user=user).order_by('-id')[:self.history_length].values_list("id", flat=True)
        PreviousPassword.objects.filter(django_user=user).exclude(pk__in=list(previous_password_ids)).delete()

    def get_help_text(self):
        return _("Your password must be different than the previous %(history_length)d passwords you have used." % {'history_length': self.history_length, })


# Allowed file extension validator
class FileExtensionValidator(RegexValidator):
    def __init__(self, extensions=settings.UPLOAD_FILE_EXTENSIONS, message=None):

        regex = '\.(%s)$' % '|'.join(extensions)
        message = 'File type not supported. Accepted types are: %s.' % ', '.join(extensions)
        super(FileExtensionValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(FileExtensionValidator, self).__call__(value.name)