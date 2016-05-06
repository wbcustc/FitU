from django.db import models

# Create your models here.

class PhotoRecord(models.Model):
	username = models.CharField(max_length=30)
	photoId = models.CharField(max_length=100)
	photoUrl = models.CharField(max_length=200)
	x = models.FloatField()
	y = models.FloatField()
	buyLink = models.CharField(max_length=1000, default=r'https://www.amazon.com')
	brand = models.CharField(max_length=100, default='Unknown')
	height = models.FloatField(default = 175)
	weight = models.FloatField(default = 70)
	shape = models.CharField(default = 'Banana', max_length=100)
	gender = models.CharField(default = 'Female', max_length=100)
