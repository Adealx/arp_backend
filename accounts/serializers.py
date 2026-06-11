from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        default='sales',
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role', 'sales')
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        # Profile is auto-created by signal; update role
        try:
            user.profile.role = role
            user.profile.save(update_fields=['role'])
        except Exception:
            pass
        return user


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role"
        ]

    def get_role(self, obj):
        return obj.profile.role


class CreateUserSerializer(serializers.ModelSerializer):

    role = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "role"
        ]

    def create(self, validated_data):

        role = validated_data.pop("role")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        user.profile.role = role
        user.profile.save()

        return user
