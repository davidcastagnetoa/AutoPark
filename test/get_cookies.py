from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import os
import sys
import pickle
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


# Cargando credenciales de acceso
load_dotenv()
MICROSOFT_ID = os.getenv("MICROSOFT_ID")
MICROSOFT_PASS = os.getenv("MICROSOFT_PASS")

# Configuración de las opciones de Firefox para el modo headless
firefox_options = Options()
# firefox_options.add_argument("--headless")
# firefox_options.add_argument("--no-sandbox")
# firefox_options.add_argument("--disable-dev-shm-usage")

# Especificando la ruta de geckodriver con Service
# service = Service('/home/admin/documents/AutoPark/downloads/geckodriver') #For Production in AWS
# driver = webdriver.Firefox(service=service, options=firefox_options) #For Production in AWS
driver = webdriver.Firefox(options=firefox_options)


def get_cookies():
    try:
        # Inicializando el driver de Firefox con las opciones configuradas
        driver.get("https://app-officemanager.raona.com/")

        # Iniciando sesion con Cuenta Office 365
        try:
            # Espera hasta que el botón de inicio de sesión de Office 365 esté presente y luego haz clic
            login_365_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MultiTenantADExchange")))
            login_365_button.click()
            print("Iniciando sesión con cuenta 365 Office ...")
        except TimeoutException:
            print("El elemento MultiTenantADExchange no está disponible en la página.")

        inputUserName = "i0116"
        buttonNext = "idSIButton9"
        inputPassword = "i0118"
        signInButton = "idSIButton9"
        verifyButton = "idSubmit_SAOTCC_Continue"
        yes_button = "idSIButton9"
        checkBoxInput = "KmsiCheckboxField"

        # Da tiempo a que la primera página se cargue
        # Espera hasta que el boton "next" esté presente
        try:
            login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, buttonNext))
            )
        except TimeoutException as e:
            print("Timeout: Boton de siguiente no encontrado dentro del tiempo esperado.", str(e))
            driver.quit()
            exit()
        except NoSuchElementException as e:
            print("NoSuchElement: Boton de siguiente no encontrado en la página.", str(e))
            driver.quit()
            exit()
        except Exception as e:
            print("Mapear esta excepcion", e)
            driver.quit()
            exit()

        # Inicia sesion
        try:
            # Busca el campo del nombre de usuario y envía los datos
            print("Cargando credenciales usuario ...")
            # Espera hasta que el elemento esté presente
            userNameField = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, inputUserName))
            )
            userNameField.clear()
            if MICROSOFT_ID is None:
                print("Error: MICROSOFT_ID no está definido.")
                sys.exit(1)
            userNameField.send_keys(MICROSOFT_ID)
            print("Usuario enviado correctamente.")
        except NoSuchElementException as e:
            print("No se encontró el elemento 'userName': ", str(e))

        try:
            # Busca el boton de siguiente de sesion y haz clic en él
            next_button = driver.find_element(By.ID, buttonNext)
            next_button.click()
            print("Siguiente ...")
        except NoSuchElementException as e:
            print("Boton de siguiente de sesion no encontrado.")
            print("fallo de botón siguiente ...", str(e))

        # Da tiempo a que la segunda página se cargue
        # Espera hasta que el boton "sign in" esté presente
        try:
            # Elimina el ElementClickInterceptedError, <div class="lightbox-cover disable-lightbox">
            element = driver.find_element(By.ID, signInButton)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            # Después de hacer scroll, intenta hacer clic
            element.click()

            login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, signInButton))
            )
        except TimeoutException as e:
            print("Timeout: Boton de Sign In no encontrado dentro del tiempo esperado.", str(e))
            driver.quit()
            exit()
        except NoSuchElementException as e:
            print("NoSuchElement: Boton de Sign In no encontrado en la página.", str(e))
            driver.quit()
            exit()
        except StaleElementReferenceException:
            # Si se produce StaleElementReferenceException, espera un poco y vuelve a intentar
            print("StaleElementReferenceException capturado, volviendo a intentar...")
            time.sleep(3)  # Espera un segundo
            # Vuelve a obtener la referencia del elemento y haz clic
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, signInButton))
            )
            element.click()
            login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, signInButton))
            )
        except Exception as e:
            print("Mapear esta excepcion", e)
            driver.quit()
            exit()

        try:
            # Busca el campo de la contraseña y envía los datos
            print("Cargando credenciales contraseña ...")
            # Espera hasta que el elemento esté presente
            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, inputPassword))
            )
            password_field.clear()
            if MICROSOFT_PASS is None:
                print("Error: MICROSOFT_PASS no está definido.")
                sys.exit(1)
            password_field.send_keys(MICROSOFT_PASS)
            print("Contraseña enviada correctamente.")
        except NoSuchElementException as e:
            print("Campo de la contraseña no encontrado.", str(e))

        try:
            # Busca el boton de inicio de sesion y haz clic en él
            signInButton = driver.find_element(By.ID, signInButton)
            signInButton.click()
            print("Iniciando sesion ...")
        except NoSuchElementException as e:
            print("Boton de inicio de sesion no encontrado.")
            print("fallo de inicio de sesion ...", str(e))

        # Esperando verificacion de credenciales
        try:
            # Espera hasta que el elemento esté presente y sea clickeable
            element = WebDriverWait(
                driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div[role='button'][data-value='OneWaySMS']")))
            # Haz clic en el elemento
            element.click()
        except TimeoutException:
            print("El elemento no se encontró en el tiempo esperado.")
        except StaleElementReferenceException:
            # Si se produce StaleElementReferenceException, espera un poco y vuelve a intentar
            print("StaleElementReferenceException capturado, volviendo a intentar...")
            time.sleep(2)  # Espera un segundo
            # Vuelve a obtener la referencia del elemento y haz clic
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][data-value='OneWaySMS']"))
            )
            element.click()

        print("Esperando verificacion de credenciales SMS por parte de usuario ...")
        time.sleep(50)

        try:
            # Busca el botón de siguiente de sesión y haz clic en él
            verify_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, verifyButton)))
            # Haz clic en el elemento
            verify_button.click()
            print("Verificando código SMS...")
        except NoSuchElementException as e:
            print("Botón de verificar no encontrado.")
            print("Fallo de botón verificar ...", str(e))

        try:
            # Busca el ckeckbox input y haz clic en él
            checkbox_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, checkBoxInput)))
            # Haz clic en el elemento
            checkbox_input.click()
            print("Marcando opcion de no mostrar de nuevo ...")
        except NoSuchElementException as e:
            print("Input de checkbox no encontrado.")
            print("Fallo de checkbox ...", str(e))

        try:
            # Busca el ckeckbox input y haz clic en él
            yes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, yes_button)))
            # Haz clic en el elemento
            yes_button.click()
            print("Marcando botón 'Si' ...")
        except NoSuchElementException as e:
            print("Botón de 'Si' no encontrado.")
            print("Fallo de botón 'Si' ...", str(e))

        url = driver.current_url
        print("Url actual: ", url)

        # Guardar cookies
        cookies = driver.get_cookies()
        with open('HyboCookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
        print("Las cookies han sido guardadas.")

        # Verificar si se ha logueado correctamente
        assert "https://app-officemanager.raona.com" in driver.current_url, \
            "No se pudo autenticar en Azure Active Directory."

        print("Se ha iniciado sesión correctamente.")
        driver.quit()

    except Exception as e:
        print("Error al intentar autenticarse:\n", str(e))
        driver.quit()


def login_with_cookies():
    try:
        # Cargar la página de inicio (necesaria antes de cargar las cookies)
        # driver.get("https://www.office.com/")
        driver.get("https://app-officemanager.raona.com/")

        # Cargar las cookies desde el archivo
        with open('HyboCookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies cargadas ...")

        # Navegar a la página después de cargar las cookies para restaurar la sesión
        # driver.get("https://www.office.com/")
        driver.get("https://app-officemanager.raona.com/")

        time.sleep(5)
        print("Credenciales 365 cargadas ...")
        time.sleep(5)

        print("Navegando a la aplicación de garajes...")
        driver.get("https://app-officemanager.raona.com/")

        # Iniciando sesion con Cuenta Office 365
        try:
            # Espera hasta que el botón de inicio de sesión de Office 365 esté presente y luego haz clic
            login_365_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MultiTenantADExchange")))
            login_365_button.click()
            print("Iniciando sesión con cuenta 365 Office ...")
        except TimeoutException:
            print("El elemento no está disponible en la página.")

        print("Sesión restaurada con éxito.")

    except Exception as e:
        print("Error al intentar iniciar sesión con cookies:", str(e))


get_cookies()
# time.sleep(10)
# login_with_cookies()
