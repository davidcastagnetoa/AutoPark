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
import time
import sys
from utils.logger import log, API
from halo import Halo

# Cargando credenciales de acceso
load_dotenv()
USERNAME_HYBO = os.getenv("USERNAME_HYBO")
PASSWORD_HYBO = os.getenv("PASSWORD_HYBO")
LINK = os.getenv("LINK")

# Otras variables
debug_mode = False  # Cambia a True para activar modo debug , no disponible en servidor de produccion


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

if debug_mode == False:
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

ascii_art_bart = """
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

ascii_art_eyes = '''

                                     .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!.
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$ 
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P 
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$# 
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$* 
      ^$$$B  $$$$\     $$$$$$$$$$$$   d$$R" 
        "*$bd$$$$      '*$$$$$$$$$$$o+#" 
             """"          """"""" 
             
    ╔────────────────────────────────────╗
    |  Soy el principio de la eternidad, |
    |  el tercero en cada cuento,        |
    |  estoy donde comienza el espacio   |
    |  y existo en mitad del tiempo!     |
    ┖────────────────────────────────────┙


'''


API.write_log(ascii_art_eyes)


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

firefox_options.binary_location = '/usr/bin/firefox'
driver = webdriver.Firefox(options=firefox_options)

# Abre la página web
link = LINK
driver.get(link)


def getToken():
    # Da tiempo para que la página se cargue
    API.write_log("Aplicando tiempo para carga de pagina")
    time.sleep(10)
    # Espera hasta que el elemento con el ID "next" esté presente
    API.write_log(f"Cargando página {link}")
    spinner = Halo(text=f'Cargando página {link}', spinner='dots')
    spinner.start()
    spinner.text = "Cargando datos de página"
    try:
        login_button = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.ID, "next"))
        )
        spinner.succeed('Boton de inicio de sesion encontrado')
    except TimeoutException:
        API.write_log("Timeout: Boton de inicio de sesion no encontrado dentro del tiempo esperado.")
        spinner.fail("Timeout: Boton de inicio de sesion no encontrado dentro del tiempo esperado. Fallo de inicio de sesión.")
        driver.quit()
        return None
    except NoSuchElementException:
        API.write_log("NoSuchElement: Boton de inicio de sesion no encontrado en la página.")
        spinner.fail("NoSuchElement: Boton de inicio de sesion no encontrado en la página. Fallo de inicio de sesión.")
        driver.quit()
        return None
    except Exception as e:
        API.write_log("Mapear esta excepcion: ", e)
        spinner.fail(f"{e}. Fallo de inicio de sesión.")
        driver.quit()
        return None

    # Inicia sesion
    spinner.text = "Localizando campo de usuario."
    try:
        # Busca el campo del nombre de usuario y envía los datos
        spinner.succeed("Cargando credenciales de usuario")
        username_field = driver.find_element(By.ID, "signInName")
        username_field.clear()
        if USERNAME_HYBO is None:
            API.write_log("Error: USERNAME_HYBO no está definido.")
            spinner.fail("Error: USERNAME_HYBO no está definido. Fallo de inicio de sesión.")
            driver.quit()
            return None
        username_field.send_keys(USERNAME_HYBO)
    except NoSuchElementException:
        API.write_log("Campo del nombre de usuario no encontrado.")
        spinner.fail("Campo del nombre de usuario no encontrado. Fallo de inicio de sesión.")
        driver.quit()
        return None

    spinner.text = "Localizando campo de contraseña."
    try:
        API.write_log("Cargando credenciales contraseña ...")
        spinner.succeed("Cargando credenciales de contraseña")
        # Busca el campo de la contraseña y envía los datos
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        if PASSWORD_HYBO is None:
            API.write_log("Error: PASSWORD_HYBO no está definido.")
            spinner.fail("Error: PASSWORD_HYBO no está definido. Fallo de inicio de sesión.")
            driver.quit()
            return None
        password_field.send_keys(PASSWORD_HYBO)
    except NoSuchElementException:
        API.write_log("Campo de la contraseña no encontrado.")
        spinner.fail("Campo de la contraseña no encontrado. Fallo de inicio de sesión.")
        return None

    spinner.text = "Iniciando sesión."
    try:
        # Busca el boton de inicio de sesion y haz clic en él
        login_button = driver.find_element(By.ID, "next")
        login_button.click()
        API.write_log("Iniciando sesion ...")
        spinner.succeed("Iniciando sesión")
    except NoSuchElementException:
        API.write_log("Boton de inicio de sesion no encontrado.")
        API.write_log("fallo de inicio de sesion ...")
        spinner.fail("Boton de inicio de sesion no encontrado. Fallo de inicio de sesión.")
        driver.quit()
        return None

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
    spinner.text = "Buscando datos en localStore ..."
    try:
        API.write_log("Buscando datos en localStore ...")
        WebDriverWait(driver, 30).until(
            lambda x: check_keys_in_localstorage(driver, keys_to_check)
        )
        API.write_log("Datos encontrados en localStorage")
        spinner.succeed("Datos encontrados en localStorage!")
    except TimeoutException:
        API.write_log("Las claves no se encontraron en localStorage dentro del tiempo especificado.")
        spinner.fail("Error: Las claves no se encontraron en localStorage.")
        driver.quit()
        return -1

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
        spinner.fail(f"No se han encontrado claves de busqueda de tokens: {not_found_message}")
        API.write_log(not_found_message)

    # Ahora puedes asignar los valores restantes a variables
    if len(access_and_refresh_item_values) >= 2:
        accessToken = access_and_refresh_item_values[0]
        refreshToken = access_and_refresh_item_values[1]

    spinner.text = "Extrayendo tokens ..."
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

        API.write_log(f"{credential_type_access}, Secret: {secret_access}\n")
        API.write_log(f"{credential_type_refresh}, Secret: {secret_refresh}\n")

        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        print("Cerrando Navegador")
        driver.quit()

        # Guardar los tokens en archivos separados
        with open("tokenAcceso.txt", "w") as f:
            f.write(secret_access)
        with open("tokenActualizacion.txt", "w") as f:
            f.write(secret_refresh)
        API.write_log("Tokens guardados en archivos separados")

        try:
            log("😈")
        except UnicodeEncodeError:
            print("Error al imprimir emoji. Continuando con el proceso.")
        finally:
            driver.quit()

        if secret_access is not None:
            spinner.succeed("Token obtenido!.")
            driver.quit()
            return secret_access
        else:
            API.write_log("Clave 'secret' no encontrada")
            spinner.fail("Clave 'secret' no encontrada!, Cerrando Navegador!")
            driver.quit()
            return None

    except json.JSONDecodeError:
        API.write_log("Error al decodificar la cadena JSON")
        spinner.fail(f"Error al decodificar la cadena JSON, Cerrando Navegador!")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None
    except TypeError:
        API.write_log("Tipo de dato incorrecto, se esperaba un diccionario")
        spinner.fail(f"Tipo de dato incorrecto, se esperaba un diccionario, Cerrando Navegador!")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None

    except Exception as e:
        API.write_log(f"Se produjo un error desconocido al obtener el token: {e}")
        spinner.fail(f"Se produjo un error desconocido al obtener el token: {e}, Cerrando Navegador!")
        # Cierra el navegador
        API.write_log("Cerrando Navegador")
        driver.quit()
        return None
    finally:
        driver.quit()
