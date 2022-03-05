import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from util.base_command import BaseCommand
from util.field import Field


class HomeWorkTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("headless")

        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
        self.driver.get("https://www.saucedemo.com/")

        self.base_command = BaseCommand(self.driver)

    def login(self):
        # login
        self.base_command.clear_element(Field.username_textfield)
        self.base_command.send_text_to_element(Field.username_textfield, "standard_user")
        self.base_command.clear_element(Field.username_passwordfield)
        self.base_command.send_text_to_element(Field.username_passwordfield, "secret_sauce")
        self.base_command.click_element(Field.login_button)
        self.assertEqual("Products".casefold(), self.base_command.get_element_text(
            Field.product_span).casefold())

    def add_products_and_goto_cart(self):
        # add 3 products to cart
        self.base_command.click_element(Field.add_product_btn1)
        self.base_command.click_element(Field.add_product_btn2)
        self.base_command.click_element(Field.add_product_btn3)
        # goto cart
        self.base_command.click_element(Field.goto_cart_link)
        self.assertEqual("YOUR CART".casefold(), self.base_command.get_element_text(
            Field.cart_span).casefold())

    def test_shipping(self):
        self.login()
        # change products sort order
        self.base_command.click_element(Field.products_sort_order_combobox)
        self.base_command.click_element(Field.sort_hilo_option)
        self.add_products_and_goto_cart()
        # make sure the right products are added
        self.assertEqual("Sauce Labs Fleece Jacket".casefold(), self.base_command.get_element_text(
            Field.product1_name_div).casefold())
        self.assertEqual("Sauce Labs Backpack".casefold(), self.base_command.get_element_text(
            Field.product2_name_div).casefold())
        self.assertEqual("Sauce Labs Bolt T-Shirt".casefold(), self.base_command.get_element_text(
            Field.product3_name_div).casefold())
        # checkout order
        self.base_command.click_element(Field.checkout_btn)
        self.base_command.clear_element(Field.order_firstname_input)
        self.base_command.send_text_to_element(Field.order_firstname_input, "First")
        self.base_command.clear_element(Field.order_lastname_input)
        self.base_command.send_text_to_element(Field.order_lastname_input, "Last")
        self.base_command.clear_element(Field.order_postalcode_input)
        self.base_command.send_text_to_element(Field.order_postalcode_input, "12-345")
        self.base_command.click_element(Field.continue_btn)
        # checkout overview
        # calculate item prices
        item1_price = float(self.base_command.get_element_text(
            Field.overview_item1_price_div).replace("$", ""))
        item2_price = float(self.base_command.get_element_text(
            Field.overview_item2_price_div).replace("$", ""))
        item3_price = float(self.base_command.get_element_text(
            Field.overview_item3_price_div).replace("$", ""))
        item_total_price = item1_price + item2_price + item3_price
        expected_item_price = 95.97
        self.assertAlmostEqual(first=item_total_price, second=expected_item_price,
            places=2, delta=0.01)
        # calculate tax
        total_price = float(self.base_command.get_element_text(
            Field.overview_total_price_lbl).split("$")[1])
        tax = float(self.base_command.get_element_text(
            Field.overview_tax_lbl).split("$")[1])
        calculated_tax = total_price - item_total_price
        self.assertAlmostEqual(first=tax, second=calculated_tax, delta=0.001)
        # finish order
        self.base_command.click_element(Field.overview_finish_btn)
        self.assertEqual("thank you for your order".casefold(),
             self.base_command.get_element_text(Field.order_complete_header).casefold())

    def test_display_products(self):
        self.login()
        self.add_products_and_goto_cart()
        # display products details
        for i in range(1,4):
            item_name = self.base_command.get_element_text(Field.cart_item_name_div % i)
            item_quantity = int(self.base_command.get_element_text(Field.cart_item_quantity_div % i))
            item_price = float(self.base_command.get_element_text(
                Field.cart_item_price_div % i).replace("$", ""))
            print("Item: %s, Quantity: %d, Price: %.2f" % (item_name, item_quantity, item_price))

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
