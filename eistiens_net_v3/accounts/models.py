from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Account(models.Model):
    """
    The Account where all additional info about the user is stored
    From an user object, you can access the related account with 'user.account'
    """
    user = models.OneToOneField(User, verbose_name='default_user')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
