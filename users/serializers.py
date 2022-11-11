from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models  import Token
from rest_framework.validators import UniqueValidator


#유저모델
class RegisterSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username','password','password2',)

    def validate(self,data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError(
        {"password":"password fields didn't match"}
        )
        return data

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token= Token.objects.create(user=user)
        return user

#로그인
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(required=True)
    password= serializers.CharField(required=True, write_only=True)
    #write_only 옵션을 통해 클라이언트-> 서버 방향 역직렬화만 가능하도록 함

    def validate(self,data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)#토큰에서 유저 찾아 응답
            return token
        raise serializers.ValidationError(
    {"error":"Unable to log in with provided credentials."})

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname",)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname",)