from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
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

# Configuracion de las opciones de Firefox para el modo headless
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
            # Espera hasta que el boton de inicio de sesion de Office 365 este presente y luego haz clic
            login_365_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "MultiTenantADExchange")))
            login_365_button.click()
            print("Iniciando sesion con cuenta 365 Office ...")
        except TimeoutException:
            print("El elemento MultiTenantADExchange no esta disponible en la pagina.")

        inputUserName = "i0116"
        buttonNext = "idSIButton9"
        inputPassword = "i0118"
        signInButton = "idSIButton9"
        verifyButton = "idSubmit_SAOTCC_Continue"
        yes_button = "idSIButton9"
        checkBoxInput = "KmsiCheckboxField"

        # Da tiempo a que la primera pagina se cargue
        # Espera hasta que el boton "next" este presente
        try:
            login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, buttonNext))
            )
        except TimeoutException as e:
            print("Timeout: Boton de siguiente no encontrado dentro del tiempo esperado.", str(e))
            driver.quit()
            exit()
        except NoSuchElementException as e:
            print("NoSuchElement: Boton de siguiente no encontrado en la pagina.", str(e))
            driver.quit()
            exit()
        except Exception as e:
            print("Mapear esta excepcion", e)
            driver.quit()
            exit()

        # Inicia sesion
        try:
            # Busca el campo del nombre de usuario y envia los datos
            print("Cargando credenciales usuario ...")
            # Espera hasta que el elemento este presente
            userNameField = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, inputUserName))
            )
            userNameField.clear()
            if MICROSOFT_ID is None:
                print("Error: MICROSOFT_ID no esta definido.")
                sys.exit(1)
            userNameField.send_keys(MICROSOFT_ID)
            print("Usuario enviado correctamente.")
        except NoSuchElementException as e:
            print("No se encontro el elemento 'userName': ", str(e))

        try:
            # Busca el boton de siguiente de sesion y haz clic en el
            next_button = driver.find_element(By.ID, buttonNext)
            next_button.click()
            print("Siguiente ...")
        except NoSuchElementException as e:
            print("Boton de siguiente de sesion no encontrado.")
            print("fallo de boton siguiente ...", str(e))

        # Da tiempo a que la segunda pagina se cargue
        # Espera hasta que el boton "sign in" este presente
        try:
            # Elimina el ElementClickInterceptedError, <div class="lightbox-cover disable-lightbox">
            element = driver.find_element(By.ID, signInButton)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            # Despues de hacer scroll, intenta hacer clic
            element.click()

            login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, signInButton))
            )
        except TimeoutException as e:
            print("Timeout: Boton de Sign In no encontrado dentro del tiempo esperado.", str(e))
            driver.quit()
            exit()
        except NoSuchElementException as e:
            print("NoSuchElement: Boton de Sign In no encontrado en la pagina.", str(e))
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
            # Busca el campo de la contraseña y envia los datos
            print("Cargando credenciales contraseña ...")
            # Espera hasta que el elemento este presente
            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, inputPassword))
            )
            password_field.clear()
            if MICROSOFT_PASS is None:
                print("Error: MICROSOFT_PASS no esta definido.")
                sys.exit(1)
            password_field.send_keys(MICROSOFT_PASS)
            print("Contraseña enviada correctamente.")
        except NoSuchElementException as e:
            print("Campo de la contraseña no encontrado.", str(e))

        try:
            # Busca el boton de inicio de sesion y haz clic en el
            signInButton = driver.find_element(By.ID, signInButton)
            signInButton.click()
            print("Iniciando sesion ...")
        except NoSuchElementException as e:
            print("Boton de inicio de sesion no encontrado.")
            print("fallo de inicio de sesion ...", str(e))

        # Esperando verificacion de credenciales
        try:
            # Espera hasta que el elemento este presente y sea clickeable
            element = WebDriverWait(
                driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div[role='button'][data-value='OneWaySMS']")))
            # Haz clic en el elemento
            element.click()
        except TimeoutException:
            print("El elemento no se encontro en el tiempo esperado.")
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
            # Busca el boton de siguiente de sesion y haz clic en el
            verify_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, verifyButton)))
            # Haz clic en el elemento
            verify_button.click()
            print("Verificando codigo SMS...")
        except NoSuchElementException as e:
            print("Boton de verificar no encontrado.")
            print("Fallo de boton verificar ...", str(e))

        try:
            # Busca el ckeckbox input y haz clic en el
            checkbox_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, checkBoxInput)))
            # Haz clic en el elemento
            checkbox_input.click()
            print("Marcando opcion de no mostrar de nuevo ...")
        except NoSuchElementException as e:
            print("Input de checkbox no encontrado.")
            print("Fallo de checkbox ...", str(e))

        try:
            # Busca el ckeckbox input y haz clic en el
            yes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, yes_button)))
            # Haz clic en el elemento
            yes_button.click()
            print("Marcando boton 'Si' ...")
        except NoSuchElementException as e:
            print("Boton de 'Si' no encontrado.")
            print("Fallo de boton 'Si' ...", str(e))

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

        print("Se ha iniciado sesion correctamente.")
        driver.quit()

    except Exception as e:
        print("Error al intentar autenticarse:\n", str(e))
        driver.quit()


def login_with_cookies():
    try:
        # Cargar las cookies desde el archivo
        with open('HyboCookies.pkl', 'rb') as file:
            cookies = pickle.load(file)

        # Cargar la pagina de 'app-officemanager.raona.com' y establecer sus cookies
        driver.get("https://app-officemanager.raona.com/")
        for cookie in cookies:
            if ".app-officemanager.raona.com" in cookie['domain']:
                driver.add_cookie(cookie)
            if "app-officemanager.raona.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de app-officemanager.raona.com cargadas ...")

        # Cargar la pagina de 'manageroffice.b2clogin.com' y establecer sus cookies
        driver.get("https://manageroffice.b2clogin.com/manageroffice.onmicrosoft.com/b2c_1a_signup_signin_custom/oauth2/v2.0/authorize?client_id=53416a92-85aa-4c86-bde0-3c06a7fd8c00&scope=https%3A%2F%2Fmanageroffice.onmicrosoft.com%2Fapi%2Faccess_as_user%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fapp-officemanager.raona.com%2F&client-request-id=ccf93630-44dd-45a7-9c4a-b0aa4645484f&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.30.0&client_info=1&code_challenge=FCFDVWfeMW_Y84Gc4cOoqoop2MK_z6x_ePYaBlYsxdQ&code_challenge_method=S256&nonce=82907033-71c5-4199-9b40-dd36b73844fb&state=eyJpZCI6IjFkYTk0MjEzLTFjMTYtNDBjMy1hYzViLWVjNGFkYjFhOGE5ZiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D")
        for cookie in cookies:
            if ".manageroffice.b2clogin.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de manageroffice.b2clogin.com cargadas ...")

        # Cargar la pagina de 'login.microsoftonline.com' y establecer sus cookies
        driver.get("https://login.microsoftonline.com/")
        for cookie in cookies:
            if "login.microsoftonline.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de login.microsoftonline.com cargadas ...")

        driver.get("https://www.microsoft.com/")
        for cookie in cookies:
            if ".microsoft.com" in cookie['domain']:
                driver.add_cookie(cookie)
            if "www.microsoft.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de microsoft.com cargadas ...")

        driver.get("https://www.office.com/")
        for cookie in cookies:
            if "www.office.com" in cookie['domain']:
                driver.add_cookie(cookie)
            if ".office.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de office.com cargadas ...")

        driver.get("https://login.live.com/")
        for cookie in cookies:
            if "login.live.com" in cookie['domain']:
                driver.add_cookie(cookie)
            if "login.live.com" in cookie['domain']:
                driver.add_cookie(cookie)
        print("Cookies de login.live cargadas ...")

        # Navegar a la pagina despues de cargar las cookies para restaurar la sesion
        driver.get("https://app-officemanager.raona.com/")

        # Iniciando sesion con Cuenta Office 365
        try:
            # Espera hasta que el boton de inicio de sesion de Office 365 este presente y luego haz clic
            login_365_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "MultiTenantADExchange")))
            login_365_button.click()
            print("Iniciando sesion con cuenta 365 Office ...")
        except TimeoutException:
            print("El elemento no esta disponible en la pagina.")

        print("Sesion restaurada con exito.")

    except Exception as e:
        print("Error al intentar iniciar sesion con cookies:", str(e))


def save_cookies(driver, domains):
    all_cookies = []
    for domain in domains:
        try:
            # Navega a cada dominio
            driver.get(domain)
            time.sleep(45)  # Ajusta este tiempo segun sea necesario
            print("Cookie capturadas en: ", domain)

            # Recoge las cookies de ese dominio
            cookies = driver.get_cookies()
            all_cookies.extend(cookies)

        except Exception as e:
            print(f"Error al intentar guardar las cookies de {domain}:", str(e))

    # Guardar todas las cookies recogidas en un archivo
    with open('HyboCookies.pkl', 'wb') as file:
        pickle.dump(all_cookies, file)
    print("Todas las cookies han sido guardadas.")


# Ejemplo de uso
domains = [
    "https://app-officemanager.raona.com/", "https://app-officemanager.raona.com/",
    "https://manageroffice.b2clogin.com/manageroffice.onmicrosoft.com/b2c_1a_signup_signin_custom/oauth2/v2.0/authorize?client_id=53416a92-85aa-4c86-bde0-3c06a7fd8c00&scope=https%3A%2F%2Fmanageroffice.onmicrosoft.com%2Fapi%2Faccess_as_user%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fapp-officemanager.raona.com%2F&client-request-id=ccf93630-44dd-45a7-9c4a-b0aa4645484f&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.30.0&client_info=1&code_challenge=FCFDVWfeMW_Y84Gc4cOoqoop2MK_z6x_ePYaBlYsxdQ&code_challenge_method=S256&nonce=82907033-71c5-4199-9b40-dd36b73844fb&state=eyJpZCI6IjFkYTk0MjEzLTFjMTYtNDBjMy1hYzViLWVjNGFkYjFhOGE5ZiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D",
    "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=fd9548d1-db02-40d0-b784-bbc8a15078ff&redirect_uri=https%3A%2F%2Fmanageroffice.b2clogin.com%2Fmanageroffice.onmicrosoft.com%2Foauth2%2Fauthresp&response_type=code&scope=profile+openid&response_mode=form_post&nonce=l%2Bqj%2FTt3l91nNKLJEB1CwQ%3D%3D&state=StateProperties%3DeyJTSUQiOiJ4LW1zLWNwaW0tcmM6ZDIzNDFiNGEtMTEzOS00ZTMxLWFjMmMtZjIxOWQ4ZDM4OTQwIiwiVElEIjoiZmY0NjI0YmMtYTZiNy00M2UxLTg4MzQtN2Q3MjVjMTYxNGVlIiwiVE9JRCI6IjQ1ODQ5MmViLWYyOGItNDE0ZC05OGRkLTFiZjMxYTdiNDUzZiJ9"
    "https://www.office.com/", "https://www.live.com/", "https://www.microsoft.com/", "https://login.microsoftonline.com/"]

# https://manageroffice.b2clogin.com/manageroffice.onmicrosoft.com/b2c_1a_signup_signin_custom/oauth2/v2.0/authorize?client_id=53416a92-85aa-4c86-bde0-3c06a7fd8c00&scope=https%3A%2F%2Fmanageroffice.onmicrosoft.com%2Fapi%2Faccess_as_user%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fapp-officemanager.raona.com%2F&client-request-id=ccf93630-44dd-45a7-9c4a-b0aa4645484f&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.30.0&client_info=1&code_challenge=FCFDVWfeMW_Y84Gc4cOoqoop2MK_z6x_ePYaBlYsxdQ&code_challenge_method=S256&nonce=82907033-71c5-4199-9b40-dd36b73844fb&state=eyJpZCI6IjFkYTk0MjEzLTFjMTYtNDBjMy1hYzViLWVjNGFkYjFhOGE5ZiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D


# save_cookies(driver, domains)
# get_cookies()
# time.sleep(10)
login_with_cookies()


# 27 coockies
