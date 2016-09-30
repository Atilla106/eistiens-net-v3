from django.contrib import messages
from django.contrib.auth import SESSION_KEY
from django.http import HttpResponse

from accounts.views import CustomAuthenticationForm
from common.tests.base import CustomUnitTestCase

from unittest.mock import patch


@patch.object(CustomAuthenticationForm, 'is_valid')
class LoginViewTest(CustomUnitTestCase):

    def _default_login_call(self, mock_form, mock_get_user, follow=False):
        mock_form.return_value = True
        mock_get_user.return_value = self.user
        return self.client.post('/accounts/login', {
                'username': 'test',
                'password': 'password'
            },
            follow=follow
        )

    def test_renders_login_template_with_get_request(self, mock_form):
        response = self.client.get('/accounts/login')
        self.assertTemplateUsed(response, 'login.html')

    def test_uses_form_data(self, mock_form):
        mock_form.return_value = False
        self.client.post('/accounts/login', {
            'username': 'test',
            'password': 'test'
        })
        mock_form.assert_called_once_with()

    @patch.object(CustomAuthenticationForm, 'get_user')
    def test_redirects_to_home_page_when_user_found(
        self, mock_get_user, mock_form
    ):
        response = self._default_login_call(mock_form, mock_get_user)
        self.assertRedirects(response, '/')

    @patch.object(CustomAuthenticationForm, 'get_user')
    @patch('accounts.views.redirect')
    def test_redirects_to_page_within_next_parameter(
        self, mock_redirect, mock_get_user, mock_form
    ):
        mock_form.return_value = True
        mock_get_user.return_value = self.user
        mock_redirect.return_value = HttpResponse()
        self.client.post('/accounts/login?next=/test/', {
            'username': 'test',
            'password': 'password',
        })
        mock_redirect.assert_called_once_with("/test/")

    def test_renders_login_page_when_user_not_found(
       self, mock_form
    ):
        mock_form.return_value = False
        response = self.client.post('/accounts/login', {
                'username': 'test',
                'password': 'password'
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'login.html')

    def test_displays_error_message_when_user_not_found(
        self, mock_form
    ):
        mock_form.return_value = False
        response = self.client.post('/accounts/login', {
                'username': 'test',
                'password': 'password'
            },
            follow=True
        )
        self.assertContains(response, "Erreur lors de la connexion")

    @patch.object(CustomAuthenticationForm, 'get_user')
    def test_user_gets_logged_in_if_authenticate_returns_a_user(
        self, mock_get_user, mock_form
    ):
        self._default_login_call(mock_form, mock_get_user)
        self.assertEqual(self.client.session[SESSION_KEY], str(self.user.pk))

    def test_user_not_logged_in_if_no_user_found(self, mock_form):
        mock_form.return_value = False
        self.client.post('/accounts/login', {
            'username': 'test',
            'password': 'password'
        })
        self.assertNotIn(SESSION_KEY, self.client.session)

    @patch('accounts.views.messages.add_message')
    @patch.object(CustomAuthenticationForm, 'get_user')
    def test_sends_success_message_if_user_logged_in(
        self, mock_get_user, mock_message, mock_form
    ):
        response = self._default_login_call(mock_form, mock_get_user)
        mock_message.assert_called_once_with(
            response.wsgi_request,
            messages.SUCCESS,
            'Bienvenue, ' + self.user.username + " !"
        )

    @patch.object(CustomAuthenticationForm, 'get_user')
    def test_displays_success_message_if_user_logged_in(
        self, mock_get_user, mock_form
    ):
        response = self._default_login_call(mock_form, mock_get_user, True)
        self.assertContains(
            response, 'Bienvenue, ' + self.user.username + " !"
        )

    def test_doesnt_display_login_needed_when_no_next_parameter(
        self, mock_form
    ):
        response = self.client.get('/accounts/login')
        self.assertNotContains(
            response,
            "Vous avez besoin d'être connecté pour voir cette page"
        )

    def test_displays_login_needed_when_next_parameter(
        self, mock_form
    ):
        response = self.client.get('/accounts/login?next=/test/')
        self.assertContains(
            response,
            "Vous avez besoin d'être connecté pour voir cette page"
        )
