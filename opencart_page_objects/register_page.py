from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url_register = base_url + "?route=account/register"
        self.url_login = base_url + "?route=account/login"


    def register_user(self):
        self.browser.get(self.url_register)
        faker = Faker()
        form_register = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, "//form[@id='form-register']")))
        email = faker.email()
        password = faker.password()

        form_register.find_element(By.XPATH, "//input[@id='input-firstname']").send_keys(faker.first_name())
        form_register.find_element(By.XPATH, "//input[@id='input-lastname']").send_keys(faker.last_name())
        form_register.find_element(By.XPATH, "//input[@id='input-email']").send_keys(email)
        form_register.find_element(By.XPATH, "//input[@id='input-password']").send_keys(password)
        form_register.find_element(By.XPATH, "//input[@name='agree']").click()
        form_register.submit()

        WebDriverWait(self.browser, 1).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='common-success']")))

        return email, password


    def login_user(self, email, password):
        self.browser.get(self.url_login)
        form_login = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, "//form[@id='form-login']")))

        form_login.find_element(By.XPATH, "//input[@id='input-email']").send_keys(email)
        form_login.find_element(By.XPATH, "//input[@id='input-password']").send_keys(password)
        form_login.submit()

        WebDriverWait(self.browser, 1).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-account']")))
