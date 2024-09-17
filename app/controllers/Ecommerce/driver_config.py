from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os


def set_driver_config():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incoginito")
    options.add_argument("--lang=en-US")

    if (
        os.environ.get("FLASK_CONFIG") == "heroku"
        and os.environ.get("FLASK_ENV") == "heroku"
    ):
        driver = webdriver.Firefox(
            options=options,
            executable_path=os.environ.get("GECKODRIVER_PATH"),
            firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")),
        )
    else:
        driver = webdriver.Firefox(
            options=options,
            executable_path=os.environ.get("GECKODRIVER_PATH") or "C:/bin/geckodriver",
            firefox_binary=FirefoxBinary(),
        )
    return driver


# ,
