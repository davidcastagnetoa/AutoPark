from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Configuración de las opciones de Firefox para el modo headless
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# Especificando la ruta de geckodriver con Service
service = Service('/home/admin/documents/AutoPark/downloads/geckodriver')

driver = None

try:
    # Inicializando el driver de Firefox con las opciones configuradas
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get("https://www.google.com")
    print(driver.title)
finally:
    if driver:
        driver.quit()

