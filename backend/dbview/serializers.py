from fitu_backend.models import CustomUser
from rest_framework import serializers


class UserviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 
        	'email', 'weight', 'height', 'gender', 'bodyShape')
