from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class MainPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url
        self.currency = "Euro"

    def check_product_on_catalog_on_main_page(self, product_name):
        self.browser.get(self.url + "/en-gb/catalog/desktops/desktops?page=1")
        wait = WebDriverWait(self.browser, 1)

        while self.browser.find_elements(By.LINK_TEXT, ">"):
            if self.browser.find_elements(By.LINK_TEXT, product_name):
                return True
            button_next = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, ">")))
            ActionChains(self.browser).move_to_element(button_next).click().perform()
        return False


    def change_currency(self, currency):
        self.browser.get(self.url)
        self.currency = currency

        form_currency = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.XPATH, "//form[@id='form-currency']")))
        form_currency.find_element(By.XPATH, "//a[@data-bs-toggle='dropdown']").click()
        form_currency.find_element(By.PARTIAL_LINK_TEXT, currency).click()

        return self


    def check_currencies_on_main_page(self):
        signs = {
            "Euro": "€",
            "Pound Sterling": "£",
            "US Dollar": "$",
        }
        sign = signs[self.currency]
        wait = WebDriverWait(self.browser, 1)

        assert sign == wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='form-currency']/div/a/strong"))).text
        assert sign in wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header-cart"]/div/button'))).text

        prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='price']")))
        for price in prices:
            spans = price.find_elements(By.XPATH, "./span")
            for span in spans:
                assert sign in span.text
