from accounts.authentication import (
    AUTH_EISTIENS_NET_URL, AuthEistiensNetBackend
)
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch
User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = AuthEistiensNetBackend()
        self.user = User.objects.create_user(username='test', password='test')
        self.user.last_name = 'Tester'
        self.user.first_name = 'Testing'
        self.user.email = 'test@eisti.fr'
        self.user.save()

    def test_sends_request_to_auth(self, mock_post):
        self.backend.authenticate(username='test', password='test')
        mock_post.assert_called_once_with(
            AUTH_EISTIENS_NET_URL,
            data={'username': 'test', 'password': 'test'}
        )

    def test_returns_none_when_403(self, mock_post):
        mock_post.return_value.status_code = 403
        response = self.backend.authenticate(username='', password='')
        self.assertIsNone(response)

    def test_finds_existing_user(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "status": "ok",
            "user": {
                "first_name": "First",
                "last_name": "Last",
                "email": "other@eisti.fr",
                "employee_number": 0
            }
        }
        other_user = User.objects.create_user(username='other', password='pw')
        user = self.backend.authenticate(username='other', password='pw')
        self.assertEquals(user, other_user)

    def test_creates_new_user_if_necessary(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "status": "ok",
            "user": {
                "first_name": "Goddy",
                "last_name": "God",
                "email": "god@eisti.fr",
                "employee_number": 0
            }
        }
        found_user = self.backend.authenticate(username='god', password='meh')
        new_user = User.objects.get(username='god')
        self.assertEquals(new_user, found_user)


class GetUserTest(TestCase):

    def test_get_user_by_username(self):
        backend = AuthEistiensNetBackend()
        bad_user = User.objects.create_user(username='badOne', password='pw')
        bad_user.save()
        desired_user = User.objects.create_user(username='user', password='pa')
        found_user = backend.get_user('user')
        self.assertEqual(desired_user, found_user)

    def test_returns_none_if_no_user_with_that_username(self):
        backend = AuthEistiensNetBackend()
        self.assertIsNone(backend.get_user('whaterver'))
