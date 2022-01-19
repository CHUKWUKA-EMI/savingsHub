from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from users.models import User
from django.conf import settings
import jwt


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        data = auth_header.decode('utf-8')
        auth_data = data.split(" ")
        if len(auth_data) != 2:
            raise exceptions.AuthenticationFailed('Invalid Authorization header')

        auth_token = auth_data[1]
        try:
            decoded_jwt_payload = jwt.decode(auth_token, settings.JWT_SECRET_KEY, algorithms="HS256")
            username = decoded_jwt_payload['username']
            user = User.objects.get(username=username)
            return (user, auth_token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
    