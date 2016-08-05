from django.contrib.auth import get_user_model
from django.urls import reverse

from .base import CustomUnitTestCase

User = get_user_model()


class HomePageTest(CustomUnitTestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_displays_logout_link_when_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertContains(
            response,
            "<a id='id_logout' href='%s'>Se déconnecter" % reverse('logout'),
            html=True
        )

    def test_home_page_displays_login_link_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertContains(
            response,
            "<a id='id_login' href='%s'>Se connecter" % reverse('login'),
            html=True
        )

    def test_home_page_displays_username_when_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertContains(
            response,
            "<nav class='navbar'>%s" % self.user.username,
            html=True
        )
