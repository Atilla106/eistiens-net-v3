from common.tests.base import CustomUnitTestCase
from django.contrib.auth import get_user_model

from accounts.models import Account

User = get_user_model()


class UserModelTest(CustomUnitTestCase):

    def test_user_model_has_username_and_password(self):
        self.assertTrue(hasattr(self.user, 'username'))
        self.assertTrue(hasattr(self.user, 'password'))


class AccountModelTest(CustomUnitTestCase):

    def test_account_model_has_user_field(self):
        account = Account(user=self.user)
        self.assertTrue(hasattr(account, 'user'))

    def test_account_model_is_created_when_user_is_created(self):
        self.assertIsNotNone(Account.objects.get(user=self.user))

    def test_user_model_has_related_account(self):
        self.assertIsNotNone(self.user.account)
