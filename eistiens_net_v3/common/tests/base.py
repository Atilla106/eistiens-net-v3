from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUnitTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='test', password='test')
        self.user.last_name = 'Tester'
        self.user.first_name = 'Testing'
        self.user.email = 'test@eisti.fr'
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        self.user.save()
