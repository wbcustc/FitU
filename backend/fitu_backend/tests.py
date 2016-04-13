from django.test import TestCase
# Create your tests here.
from models import CustomUser
from rest_framework.authtoken.models import Token

# for user in CustomUser.objects.all():
#     Token.objects.get_or_create(user=user)

# testUser = CustomUser.objects.create_user(username='wbcustc1', 
# 	email='bw475@cornell.edu', password='123456',
# 	height=180, weight=83)
