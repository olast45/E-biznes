import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class SauceDemoTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.quit()

    def login(self, username="standard_user", password="secret_sauce"):
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    def test_successful_login_redirects_to_inventory(self):
        self.login()
        self.assertIn("inventory", self.driver.current_url)

    def test_failed_login_shows_error_message(self):
        self.login(password="wrong_password")
        error = self.driver.find_element(By.CLASS_NAME, "error-message-container")
        self.assertTrue(error.is_displayed())

    def test_inventory_page_has_six_products(self):
        self.login()
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.assertEqual(len(items), 6)

    def test_product_names_are_visible_on_inventory_page(self):
        self.login()
        names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        self.assertEqual(len(names), 6)
        for name in names:
            self.assertTrue(name.is_displayed())

    def test_adding_product_to_cart_updates_cart_count(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        cart = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(cart.text, "1")

    def test_removing_product_from_cart_clears_cart(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "btn_secondary").click()
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(cart_badge), 0)

    def test_accessing_cart_page(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.assertIn("cart", self.driver.current_url)

    def test_logout_redirects_to_login_page(self):
        self.login()
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        sleep(1)
        self.driver.find_element(By.ID, "logout_sidebar_link").click()
        self.assertIn("saucedemo.com", self.driver.current_url)

    def test_product_detail_page_opens_on_click(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
        self.assertIn("inventory-item", self.driver.current_url)

    def test_add_multiple_products_to_cart_updates_cart_count(self):
        self.login()
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn_inventory")[:3]
        for btn in buttons:
            btn.click()
        cart = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(cart.text, "3")

    def test_checkout_button_is_visible_in_cart(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.assertTrue(self.driver.find_element(By.ID, "checkout").is_displayed())

    def test_checkout_form_accepts_user_data(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.driver.find_element(By.ID, "first-name").send_keys("Jan")
        self.driver.find_element(By.ID, "last-name").send_keys("Kowalski")
        self.driver.find_element(By.ID, "postal-code").send_keys("00-001")
        self.driver.find_element(By.ID, "continue").click()
        self.assertIn("checkout-step-two", self.driver.current_url)

    def test_cancel_checkout_redirects_to_cart_page(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.driver.find_element(By.ID, "cancel").click()
        self.assertIn("cart", self.driver.current_url)

    def test_completing_purchase_redirects_to_complete_page(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.driver.find_element(By.ID, "first-name").send_keys("Test")
        self.driver.find_element(By.ID, "last-name").send_keys("User")
        self.driver.find_element(By.ID, "postal-code").send_keys("12345")
        self.driver.find_element(By.ID, "continue").click()
        self.driver.find_element(By.ID, "finish").click()
        self.assertIn("checkout-complete", self.driver.current_url)

    def test_checkout_form_shows_error_when_fields_are_empty(self):
        self.login()
        self.driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.driver.find_element(By.ID, "continue").click()
        error = self.driver.find_element(By.CLASS_NAME, "error-message-container")
        self.assertTrue(error.is_displayed())

    def test_sorting_dropdown_is_visible_on_inventory_page(self):
        self.login()
        sort = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        self.assertTrue(sort.is_displayed())

    def test_cart_badge_is_hidden_when_cart_is_empty(self):
        self.login()
        badges = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(badges), 0)

    def test_menu_expands_when_clicked(self):
        self.login()
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        sleep(1)
        menu = self.driver.find_element(By.CLASS_NAME, "bm-menu-wrap")
        self.assertTrue(menu.is_displayed())

    def test_twitter_link_is_visible_and_valid(self):
        self.login()
        twitter = self.driver.find_element(By.CSS_SELECTOR, "a[href*='twitter.com']")
        self.assertTrue(twitter.is_displayed())
        self.assertIn("twitter.com", twitter.get_attribute("href"))

    def test_each_product_has_a_name_and_price(self):
        self.login()
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name")
            price = item.find_element(By.CLASS_NAME, "inventory_item_price")
            self.assertTrue(name.text)
            self.assertTrue(price.text.startswith("$"))

if __name__ == "__main__":
    unittest.main()
