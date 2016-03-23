from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

GENDER_CHOICES = (
	(1, u'Female'),
	(2, u'Male'),
)

class CustomUser(AbstractUser):
	weight = models.FloatField()
	height = models.FloatField()
	gender = models.CharField(choices = GENDER_CHOICES, max_length=10)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)