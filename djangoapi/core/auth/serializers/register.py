from rest_framework import serializers

from core.user.serializers import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        min_length=8,
        required=True,
    )

    class Meta:
        model = User

        fields = ['id', 'bio', 'avatar', 'email', 'username', 'first_name',
                  'last_name', 'password', 'is_superuser']

    def create(self, validated_data):
        if validated_data['is_superuser'] == True:
            return User.objects.createSuperUser(**validated_data)

        return User.objects.createUser(**validated_data)