
from selenium.webdriver.common.by import By
from utils.base_class import *

from utils.env_config import env_config


class LoginPage:
    USERNAME_INPUT_LOCATOR = "//input[@type='email']"
    PASSWORD_INPUT_LOCATOR = "//input[@type='password']"
    LOGIN_BUTTON_LOCATOR = "//button[normalize-space()='SIGN IN']"

    def __init__(self, driver):
        self.driver = driver
        self.env = env_config()

    def launch_url(self):
        self.driver.get(self.env.get('BASE_URL'))

    def provide_email_and_password(self, username, password):

        if username:
            self.driver.find_element(By.XPATH, self.USERNAME_INPUT_LOCATOR).clear()
            self.driver.find_element(By.XPATH, self.USERNAME_INPUT_LOCATOR).send_keys(username)

        if password:
            self.driver.find_element(By.XPATH, self.PASSWORD_INPUT_LOCATOR).clear()
            self.driver.find_element(By.XPATH, self.PASSWORD_INPUT_LOCATOR).send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, self.LOGIN_BUTTON_LOCATOR).click()
        allure_attach_screenshot(self)
