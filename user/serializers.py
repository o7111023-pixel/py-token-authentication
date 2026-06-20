from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserManageSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        required=False,
        style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "email",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
