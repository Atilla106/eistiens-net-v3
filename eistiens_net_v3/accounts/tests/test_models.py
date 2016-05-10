from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_model_has_username_and_password(self):
        user = User('test', 'test')
        self.assertTrue(hasattr(user, 'username'))
        self.assertTrue(hasattr(user, 'password'))
