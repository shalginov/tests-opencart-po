from opencart_page_objects.register_page import RegisterPage

def test_register_user(browser, base_url):
    register_page = RegisterPage(browser, base_url)

    creds = register_page.register_user()
    register_page.login_user(*creds)