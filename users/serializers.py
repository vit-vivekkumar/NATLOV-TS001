from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "password",
        ]

    def create(self, validated_data):
        # Hash the password before saving the user
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
