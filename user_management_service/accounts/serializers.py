from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_repeat", "gender")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError({"password": "The passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            gender=validated_data.get("gender")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "gender", "first_name", "last_name") 