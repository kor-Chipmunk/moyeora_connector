from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User

class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                       validated_data['nickname'],
                                       validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ['email', 'nickname', 'password']
        extra_kwargs = {'password': { 'write_only': True }}

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs, ):
        user = authenticate(
            email=attrs['email'], password=attrs['password']
        )

        if user is None:
            raise serializers.ValidationError('invalid credentials provided')
        self.instance = user
        return user

class UserNicknameSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'nickname',)