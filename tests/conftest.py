import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="choose browser",
        choices=("chrome", "firefox", "yandex")
    )
    parser.addoption(
        "--url",
        action="store",
        default="http://192.168.27.17:8081/",
        help="define url string"
    )


@pytest.fixture()
def browser(request):
    cmdopt = request.config.getoption("browser")
    if cmdopt == "chrome":
        driver = webdriver.Chrome()
    elif cmdopt == "firefox":
        driver = webdriver.Firefox()
    elif cmdopt == "yandex":
        options = webdriver.ChromeOptions()
        options.binary_location("yandex_browser_directory/yandex.exe")
        service = Service(executable_path="yandex_driver-directory/yandexdriver.exe")
        driver = webdriver.Chrome(options=options, service=service)
    else:
        print("browser is not supported, Chrome is chosen")
        driver = webdriver.Chrome()

    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture
def base_url(request):
    return request.config.getoption("url")