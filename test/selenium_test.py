from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from utils.logger import log, API


firefox_options = Options()
firefox_capabilities = firefox_options.to_capabilities()

# Headless mode Firefox
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://www.google.com")
    log(driver.title)
    API.write_log(driver.title)
finally:
    driver.quit()
