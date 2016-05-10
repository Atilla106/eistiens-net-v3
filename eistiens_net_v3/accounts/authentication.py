from django.contrib.auth import get_user_model
import requests

User = get_user_model()
AUTH_EISTIENS_NET_URL = 'http://auth.eistiens.net'


class AuthEistiensNetBackend():
    def authenticate(self, username, password):
        response = requests.post(
            AUTH_EISTIENS_NET_URL,
            data={'username': username, 'password': password}
        )
        if response.status_code == 200:
            try:
                u = User.objects.get(username=username)
                return User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user_data = response.json()['user']
                user.last_name = user_data['last_name']
                user.first_name = user_data['first_name']
                user.email = user_data['email']
                user.backend = accounts.AuthEistiensNetBackend
                user.save()
                return user

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
