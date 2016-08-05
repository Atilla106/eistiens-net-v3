from django.contrib.auth import get_user_model

from accounts.authentication import AuthEistiensNetBackend
from portal.tests.base import CustomUnitTestCase

from unittest.mock import patch

User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticateTest(CustomUnitTestCase):

    def setUp(self):
        self.backend = AuthEistiensNetBackend()

    def test_sends_request_to_auth(self, mock_post):
        self.backend.authenticate(username='test', password='test')
        mock_post.assert_called_once_with(
            self.backend.AUTH_EISTIENS_NET_URL,
            data={'username': 'test', 'password': 'test'}
        )

    def test_returns_none_when_403(self, mock_post):
        mock_post.return_value.status_code = 403
        response = self.backend.authenticate(username='', password='')
        self.assertIsNone(response)

    def test_returns_none_when_empty_response(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}
        response = self.backend.authenticate(username='', password='')
        self.assertIsNone(response)

    def test_returns_none_when_incorrect_response(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "not_user": {
                "first_name": "First",
                "last_name": "Last",
                "email": "other@eisti.fr",
                "employee_number": 0
            }
        }
        user = self.backend.authenticate(username='test', password='test')
        self.assertIsNone(user)

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
        self.assertEqual(user, other_user)

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
        self.assertEqual(new_user, found_user)

    def test_returns_none_when_server_not_reachable(self, mock_post):
        mock_post.side_effect = ConnectionError
        user = self.backend.authenticate(username='test', password='test')
        self.assertIsNone(user)


class GetUserTest(CustomUnitTestCase):

    def test_get_user_by_username(self):
        backend = AuthEistiensNetBackend()
        user = User.objects.get(pk=1)
        found_user = backend.get_user(1)
        self.assertEqual(user, found_user)

    def test_returns_none_if_no_user_with_that_id(self):
        backend = AuthEistiensNetBackend()
        self.assertIsNone(backend.get_user(2))
