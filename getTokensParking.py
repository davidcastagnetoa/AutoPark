# import inquirer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import json
from dotenv import load_dotenv
import os
import sys
from utils.logger import log, API

# Cargando credenciales de acceso
load_dotenv()
USERNAME_HYBO = os.getenv("USERNAME_HYBO")
PASSWORD_HYBO = os.getenv("PASSWORD_HYBO")
LINK = os.getenv("LINK")

# Configura las opciones para Firefox
# firefox_options = webdriver.FirefoxOptions()
firefox_options = Options()
firefox_capabilities = firefox_options.to_capabilities()

# Configura las opciones para Chrome
# chrome_options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_capabilities = chrome_options.to_capabilities()

# Headless mode Chrome
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Headless mode Firefox
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# questions = [
#     inquirer.List(
#         "navegator",
#         message="Elije un navegador",
#         choices=["Chrome", "Firefox", "Cancelar"],
#     ),
# ]
ascii_art = """
         , ,\ ,'\,'\ ,'\ ,\ ,
   ,  ;\/ \/ \`'     `   '  /|
   |\/                      |
   :                        |
   :                        |
    |                       |
    :               -.     _|
     :                \     `.
     |         ________:______\.
     :       ,'o       / o    ;
     :       \       ,'-----./
      \_      `--.--'        )
     ,` `.              ,---'|
     : `                     |
      `,-'                   |
      /      ,---.          ,'
   ,-'            `-,------'   Developed By 
  '   `.        ,--'           AbathurCris!
 '     `-.____/
/           \.
"""
API.write_log(ascii_art)
API.write_log("\n__CONSULTA DE TOKEN__")

# answers = inquirer.prompt(questions)
# navegador = answers["navegator"]

# if navegador == "Chrome":
#     API.write_log("Iniciando navegador Chrome")
#     driver = webdriver.Chrome(options=chrome_options)
# elif navegador == "Firefox":
#     API.write_log("Iniciando navegador Firefox")
#     driver = webdriver.Firefox(options=firefox_options)
# else:
#     API.write_log("Operacion cancelada por el usuario.")
#     exit()


# Usar Chrome/Firefox por defecto, sin interaccion del usuario
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Firefox(options=firefox_options)

# Abre la página web
link = LINK
driver.get(link)


def getToken():
    # Da tiempo para que la página se cargue
    # Espera hasta que el elemento con el ID "next" esté presente
    API.write_log(f"Cargando página {link}")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "next"))
        )
    except TimeoutException:
        API.write_log("Timeout: Boton de inicio de sesion no encontrado dentro del tiempo esperado.")
        driver.quit()
        exit()
    except NoSuchElementException:
        API.write_log("NoSuchElement: Boton de inicio de sesion no encontrado en la página.")
        driver.quit()
        exit()
    except Exception as e:
        print("Mapear esta excepcion", e)
        driver.quit()
        exit()

    # Inicia sesion
    try:
        # Busca el campo del nombre de usuario y envía los datos
        username_field = driver.find_element(By.ID, "signInName")
        username_field.clear()
        if USERNAME_HYBO is None:
            API.write_log("Error: USERNAME_HYBO no está definido.")
            sys.exit(1)
        username_field.send_keys(USERNAME_HYBO)
    except NoSuchElementException:
        API.write_log("Campo del nombre de usuario no encontrado.")

    try:
        API.write_log("Cargando credenciales contraseña ...")
        # Busca el campo de la contraseña y envía los datos
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        if PASSWORD_HYBO is None:
            API.write_log("Error: USERNAME_HYBO no está definido.")
            sys.exit(1)
        password_field.send_keys(PASSWORD_HYBO)
    except NoSuchElementException:
        API.write_log("Campo de la contraseña no encontrado.")

    try:
        # Busca el boton de inicio de sesion y haz clic en él
        login_button = driver.find_element(By.ID, "next")
        login_button.click()
        API.write_log("Iniciando sesion ...")
    except NoSuchElementException:
        API.write_log("Boton de inicio de sesion no encontrado.")
        API.write_log("fallo de inicio de sesion ...")

    # Funcion para verificar si las claves están en localStorage

    def check_keys_in_localstorage(driver, keys):
        script = f"""
        let keysToCheck = {json.dumps(keys)};
        return keysToCheck.every(key => localStorage.getItem(key) !== null);
        """
        return driver.execute_script(script)

    # Lista de claves a verificar en localStorage
    keys_to_check = [
        "39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-accesstoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00-458492eb-f28b-414d-98dd-1bf31a7b453f-https://manageroffice.onmicrosoft.com/api/access_as_user--",
        "39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-refreshtoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00----",]

    # Espera hasta que las claves estén en localStorage o se agote el tiempo (20 segundos aquí)
    try:
        API.write_log("Extrayendo tokens ...")
        WebDriverWait(driver, 20).until(
            lambda x: check_keys_in_localstorage(driver, keys_to_check)
        )
        API.write_log("Datos encontrados en localStorage: ")
    except TimeoutException:
        API.write_log("Las claves no se encontraron en localStorage dentro del tiempo especificado.")
        driver.quit()
        sys.exit(-1)

    # Ejecuta el script para obtener el AccessToken y RefreshToken del localStorage
    access_and_refresh_item_values = driver.execute_script(
        """
        function getValuesByKeysFromLocalStorage(keys) {
            let results = [];
            let notFoundKeys = [];

            keys.forEach((key) => {
                let value = localStorage.getItem(key);
                if (value !== null) {
                    results.push(value);
                } else {
                    notFoundKeys.push(key);
                }
            });

            if (notFoundKeys.length > 0) {
                results.push("No se encontraron los siguientes keys: " + notFoundKeys.join(", "));
            }

            return results;
        }

        return getValuesByKeysFromLocalStorage(["39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-accesstoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00-458492eb-f28b-414d-98dd-1bf31a7b453f-https://manageroffice.onmicrosoft.com/api/access_as_user--", "39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-refreshtoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00----"]);
        """
    )

    # Manejar el caso en que se incluye un mensaje sobre claves no encontradas
    if "No se encontraron" in access_and_refresh_item_values[-1]:
        # Remueve y guarda el último elemento
        not_found_message = access_and_refresh_item_values.pop()
        API.write_log(not_found_message)

    # Ahora puedes asignar los valores restantes a variables
    if len(access_and_refresh_item_values) >= 2:
        accessToken = access_and_refresh_item_values[0]
        refreshToken = access_and_refresh_item_values[1]

    try:
        access_json_str = accessToken
        refresh_json_str = refreshToken

        # Convertir las cadenas JSON en diccionarios de Python
        access_dict = json.loads(access_json_str)
        refresh_dict = json.loads(refresh_json_str)

        # Extraer los valores de "credentialType" y "secret" para el token de acceso
        credential_type_access = access_dict.get(
            "credentialType", "Clave 'credentialType' no encontrada"
        )
        secret_access = access_dict.get(
            "secret", "Clave 'secret' no encontrada")

        # Extraer los valores de "credentialType" y "secret" para el token de actualización
        credential_type_refresh = refresh_dict.get(
            "credentialType", "Clave 'credentialType' no encontrada"
        )
        secret_refresh = refresh_dict.get(
            "secret", "Clave 'secret' no encontrada")

        # API.write_log(f"{credential_type_access}, Secret: {secret_access}\n")
        # API.write_log(f"{credential_type_refresh}, Secret: {secret_refresh}\n")

        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()

        # Guardar los tokens en archivos separados
        with open("tokenAcceso.txt", "w") as f:
            f.write(secret_access)
        with open("tokenActualizacion.txt", "w") as f:
            f.write(secret_refresh)
        API.write_log("Tokens guardados en archivos separados")
        log("😈")

        if secret_access is not None:
            return secret_access
        else:
            API.write_log("Clave 'secret' no encontrada")
            return None

    except json.JSONDecodeError:
        API.write_log("Error al decodificar la cadena JSON")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None
    except TypeError:
        API.write_log("Tipo de dato incorrecto, se esperaba un diccionario")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None
    except Exception as e:
        API.write_log(f"Se produjo un error desconocido: {e}")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None
