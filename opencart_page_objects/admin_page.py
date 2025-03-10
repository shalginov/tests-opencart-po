import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from faker import Faker



class AdminPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url + "/administration"



    def login_admin(self):
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, 1)
        wait.until(EC.presence_of_element_located((By.ID, "input-username"))).send_keys("user")
        wait.until(EC.presence_of_element_located((By.ID, "input-password"))).send_keys("bitnami")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"submit\"]"))).click()


    def add_product(self):
        self.login_admin()
        faker = Faker()
        name = faker.words(3)
        product_name = ' '.join(name)
        seo = '-'.join(name)
        wait = WebDriverWait(self.browser, 1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href=\"#collapse-1\"]"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Products"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"content\"]/div[1]/div/div/a"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "input-name-1"))).send_keys(product_name)
        wait.until(EC.presence_of_element_located((By.ID, "input-meta-title-1"))).send_keys("Meta Tag "+product_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"form-product\"]/ul/li[2]/a"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "input-model"))).send_keys("Model "+str(faker.random_int(10,99,1)))
        wait.until(EC.presence_of_element_located((By.ID, "input-price"))).send_keys(str(faker.pyfloat(3,2,True,10,999)))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href=\"#tab-seo\"]"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "input-keyword-0-1"))).send_keys(seo)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=\"submit\"][form=\"form-product\"]"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        return product_name


    def delete_product(self, product_name):
        self.login_admin()
        wait = WebDriverWait(self.browser, 1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href=\"#collapse-1\"]"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Products"))).click()

        while True:
            time.sleep(1) # без этого ошибка stale reference element exception
            list_products = WebDriverWait(self.browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//form[@id='form-product']//td[@class='text-start']")))
            if list_products:
                for product in list_products:
                    if product_name in product.text:
                        product.find_element(By.XPATH,"./..//input[@name=\"selected[]\"][@class=\"form-check-input\"]").click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"content\"]/div[1]/div/div/button[3]"))).click()
                        self.browser.switch_to.alert.accept()
                        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
                        return True

            if not self.browser.find_elements(By.LINK_TEXT, ">"):
                print("Product not found")
                return False
            button_next: WebElement = wait.until(EC.presence_of_element_located((By.LINK_TEXT, ">")))
            ActionChains(self.browser, 1000).move_to_element(button_next).click().perform()

