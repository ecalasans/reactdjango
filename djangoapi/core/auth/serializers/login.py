from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from core.user.serializers import UserSerializer

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("Attributes received for validation:", attrs)  # Debugging line
        try:
            data = super().validate(attrs=attrs)
            print("Data after super validation:", data)  # Debugging line
        except Exception as e:
            print("Error during validation:", str(e))  # Debugging line
            raise e

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data