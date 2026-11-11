from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'branch',
            'year',
            'batch',
            'regulation'
        ]

    def validate(self, data):
        # 🚫 Force user to provide academic details
        required_fields = ['branch', 'year', 'batch', 'regulation']

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user