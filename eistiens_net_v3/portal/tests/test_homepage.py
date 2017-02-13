from django.contrib.auth import get_user_model
from django.urls import reverse

from common.tests.base import CustomUnitTestCase

User = get_user_model()


class HomePageTest(CustomUnitTestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'portal/home.html')

    def test_home_page_displays_logout_link_when_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertContains(
            response,
            'href="%s">Déconnexion' % reverse('accounts:logout')
        )

    def test_home_page_displays_login_link_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertContains(
            response,
            'href="%s">Se connecter' % reverse('accounts:login')
        )

    def test_home_page_displays_username_when_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertContains(
            response,
            "id='username'>%s" % self.user.username
        )
