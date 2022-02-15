from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseCommand:
    def __init__(self, driver):
        self.local_driver: webdriver.Chrome = driver
        self.wait : WebDriverWait = WebDriverWait(driver, 3)

    def click_element(self, element):
        self.local_driver.find_element(By.XPATH, element).click()

    def clear_element(self, element):
        self.local_driver.find_element(By.XPATH, element).clear()

    def send_text_to_element(self, element, text):
        self.local_driver.find_element(By.XPATH, element).send_keys(text)

    def get_element_text(self, element):
        self.wait.until(EC.visibility_of_element_located( (By.XPATH, element) ))
        return self.local_driver.find_element(By.XPATH, element).text