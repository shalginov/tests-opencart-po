from opencart_page_objects.admin_page import AdminPage
from opencart_page_objects.main_page import MainPage

def test_add_product(browser, base_url):
    admin_page = AdminPage(browser, base_url)
    main_page = MainPage(browser, base_url)

    product_name = admin_page.add_product()
    main_page.check_product_on_catalog_on_main_page(product_name)
    admin_page.delete_product(product_name)
