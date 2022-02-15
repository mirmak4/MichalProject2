import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from util.base_command import BaseCommand
from util.field import Field


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("headless")

        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
        self.driver.get("https://www.saucedemo.com/")

        self.base_command = BaseCommand(self.driver)

    def test_sauce_login(self):

        self.base_command.clear_element(Field.username_textfield)
        self.base_command.send_text_to_element(Field.username_textfield, "standard_user")

        self.base_command.clear_element(Field.username_passwordfield)
        self.base_command.send_text_to_element(Field.username_passwordfield, "secret_sauce")

        self.base_command.click_element(Field.login_button)

        self.assertEqual("Products".casefold(), self.base_command.get_element_text(
            Field.product_span).casefold())

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()