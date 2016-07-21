from django.contrib.auth import get_user_model

import requests

User = get_user_model()


class AuthEistiensNetBackend():
    """
    Custom authentication backend using auth.eistiens.net.
    This allows us to not have to use directly EISTI's LDAP,
    which is not available without quite a lot of setup
    from outside EISTI's network.
    For more information on auth.eistiens.net, look at
    http://doc.atilla.org
    """
    AUTH_EISTIENS_NET_URL = 'http://auth.eistiens.net'

    def authenticate(self, username, password):
        try:
            response = requests.post(
                self.AUTH_EISTIENS_NET_URL,
                data={'username': username, 'password': password}
            )
        except ConnectionError:
            return None
        try:
            if response.status_code == 200 and \
                    response.json()['status'] == 'ok':
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
            user.save()
            return user
        except KeyError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
