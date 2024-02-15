from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


firefox_options = Options()
firefox_capabilities = firefox_options.to_capabilities()

# Headless mode Firefox
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

service = Service('/home/admin/applications/Parking_SD/AutoPark/geckodriver/geckodriver')

try:
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get("https://www.google.com")
    print(driver.title)
finally:
    driver.quit()
