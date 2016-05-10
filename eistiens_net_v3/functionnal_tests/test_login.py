from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest


class LoginTest(FunctionalTest):
    def wait_for_element_with_id(self, id):
        WebDriverWait(self.browser, timeout=5).until(
            lambda b: b.find_element_by_id(id),
            'Could not find element with id {}. Page text was :\n{}'.format(
                id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('terrienale', navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn('terrienale', navbar.text)

    def test_login_LDAP(self):
        # The student goes in the brand new website
        self.browser.get(self.server_url)

        # He notices it's called eistiens.net
        self.assertIn('eistiens.net', self.browser.title)
        # He notices a link where he can connect
        link_text = self.browser.find_element_by_tag_name('a')
        self.assertIn('Se connecter', link_text.text)
        link_text.click()

        # He sees a from where he can fill in his LDAP login
        login = self.browser.find_element_by_id('id_username')
        passwd = self.browser.find_element_by_id('id_password')
        self.assertEqual(login.get_attribute('placeholder'), 'Login LDAP')
        self.assertEqual(
                passwd.get_attribute('placeholder'),
                'Mot de passe LDAP'
        )
        # He fills in the info
        login.send_keys('terrienale')
        passwd.send_keys('E77958:terri')
        passwd.send_keys(Keys.ENTER)

        # He notices his LDAP login on the screen
        self.wait_to_be_logged_in()

        # He stays logged in even if he reloads
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # He then logs out
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # Even if he refreshes, he's still logged out
        self.browser.refresh()
        self.wait_to_be_logged_out
