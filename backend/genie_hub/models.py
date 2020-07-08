from logging import getLogger
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

logger = getLogger('genie_hub.models')

class PreviousPassword(models.Model):
    """
    Previously used password
    """
    created_on = models.DateTimeField(auto_now_add=True)
    django_user = models.ForeignKey(User, on_delet=models.CASCADE)
    password_hash = models.CharField(max_length=200)

# Hook up user login signal to record every user login
def update_user_login(sender, **kwargs):
    user = kwargs.pop('user', None)

user_logged_in.connect(update_user_login, sender=User)

# class GlobalPermissions(models.Model):
#     class Meta:
#         managed = False

#         permissions = (
#         )

@receiver(post_save)
def clear_the_cache(sender, **kwargs):
    cache.clear()