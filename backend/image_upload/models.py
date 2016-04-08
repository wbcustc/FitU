from django.db import models

# Create your models here.

class PhotoRecord(models.Model):
	username = models.CharField(max_length=30)
	photoId = models.CharField(max_length=100)
	photoUrl = models.CharField(max_length=200)
	buyLink = models.CharField(max_length=1000, default=r'https://www.amazon.com')
	brand = models.CharField(max_length=100, default='Unknown')
