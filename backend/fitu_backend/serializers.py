from models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 
        	'weight', 'height', 'gender', 'bodyShape', 'avatarUrl')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 
        	'weight', 'height', 'gender', 'bodyShape', 'avatarUrl')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser(
        	username=validated_data['username'],
            weight=validated_data['weight'],
            height=validated_data['height'],
            gender=validated_data['gender'],
            bodyShape=validated_data['bodyShape'],
        )
        user.set_password(validated_data['password'])
        print user
        user.save()
        return user