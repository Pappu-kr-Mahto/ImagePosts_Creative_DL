from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]
    
    def validate(self,data):
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError({'error': 'User already exists with this username/email '})
            return data

    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'] , email=validated_data['email'],password=validated_data['password'])
        UserProfile.objects.create(user=user,username=validated_data['username'])
        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
          model = UserProfile
          fields = '__all__'

class ImagePostSerializer(serializers.ModelSerializer):
     class Meta:
          model = ImagePost
          fields = '__all__'

class GetImagePostSerilizer(serializers.Serializer):
     image=serializers.ImageField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()