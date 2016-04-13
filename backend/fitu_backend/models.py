from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

GENDER_CHOICES = (
	(u'Female', u'Female'),
	(u'Male', u'Male'),
)

BODY_SHAPE_CHOICES = (
	(u'Pear', u'Pear'),
	(u'Apple', u'Apple'),
	(u'Banana', u'Banana')
)

class CustomUser(AbstractUser):
	weight = models.FloatField(default = 150)
	height = models.FloatField(default = 5.5)
	gender = models.CharField(choices = GENDER_CHOICES, max_length=10, default='Male')
	bodyShape = models.CharField(choices = BODY_SHAPE_CHOICES, max_length=20, default='Pear')
	avatarUrl = models.CharField(max_length = 500, default = r'https://s3.amazonaws.com/fituuseravatar/default.jpg')
	

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)