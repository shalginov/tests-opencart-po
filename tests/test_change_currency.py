import pytest
from opencart_page_objects.main_page import MainPage

@pytest.mark.parametrize("currency", ["Euro", "Pound Sterling", "US Dollar"])
def test_change_currency(browser, base_url, currency):
    main_page = MainPage(browser, base_url)
    main_page.change_currency(currency).check_currencies_on_main_page()