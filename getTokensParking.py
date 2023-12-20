# import inquirer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json
from dotenv import load_dotenv
import os


# Cargando credenciales de acceso
load_dotenv()
USERNAME_HYBO = os.getenv("USERNAME_HYBO")
PASSWORD_HYBO = os.getenv("PASSWORD_HYBO")

# Configura las opciones para Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_capabilities = firefox_options.to_capabilities()
# Configura las opciones para Chrome
chrome_options = webdriver.ChromeOptions()
chrome_capabilities = chrome_options.to_capabilities()

# questions = [
#     inquirer.List(
#         "navegator",
#         message="Elije un navegador",
#         choices=["Chrome", "Firefox", "Cancelar"],
#     ),
# ]
ascii_art = """
                                                          ..
                               ,,,                         MM .M
                           ,!MMMMMMM!,                     MM MM  ,.
   ., .M                .MMMMMMMMMMMMMMMM.,          'MM.  MM MM .M'
 . M: M;  M          .MMMMMMMMMMMMMMMMMMMMMM,          'MM,:M M'!M'
;M MM M: .M        .MMMMMMMMMMMMMMMMMMMMMMMMMM,         'MM'...'M
 M;MM;M :MM      .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.       .MMMMMMMM
 'M;M'M MM      MMMMMM  MMMMMMMMMMMMMMMMM  MMMMMM.    ,,M.M.'MMM'
  MM'MMMM      MMMMMM @@ MMMMMMMMMMMMMMM @@ MMMMMMM.'M''MMMM;MM'
 MM., ,MM     MMMMMMMM  MMMMMMMMMMMMMMMMM  MMMMMMMMM      '.MMM
 'MM;MMMMMMMM.MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.      'MMM
  ''.'MMM'  .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM       MMMM
   MMC      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.      'MMMM
  .MM      :MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM''MMM       MMMMM
  MMM      :M  'MMMMMMMMMMMMM.MMMMM.MMMMMMMMMM'.MM  MM:M.    'MMMMM
 .MMM   ...:M: :M.'MMMMMMMMMMMMMMMMMMMMMMMMM'.M''   MM:MMMMMMMMMMMM'
AMMM..MMMMM:M.    :M.'MMMMMMMMMMMMMMMMMMMM'.MM'     MM''''''''''''
MMMMMMMMMMM:MM     'M'.M'MMMMMMMMMMMMMM'.MC'M'     .MM
 '''''''''':MM.       'MM!M.'M-M-M-M'M.'MM'        MMM
            MMM.            'MMMM!MMMM'            .MM
             MMM.             '''   ''            .MM'
              MMM.                               MMM'
               MMMM            ,.J.JJJJ.       .MMM'
                MMMM.       'JJJJJJJ'JJJM   CMMMMM
                  MMMMM.    'JJJJJJJJ'JJJ .MMMMM'
                    MMMMMMMM.'  'JJJJJ'JJMMMMM'
                      'MMMMMMMMM'JJJJJ JJJJJ'
                         ''MMMMMMJJJJJJJJJJ'
                                 'JJJJJJJJ'
"""
print(ascii_art)
print("\n__CONSULTA DE TOKEN__")
# answers = inquirer.prompt(questions)
# navegador = answers["navegator"]

# if navegador == "Chrome":
#     print("Iniciando navegador Chrome")
#     driver = webdriver.Chrome(options=chrome_options)
# elif navegador == "Firefox":
#     print("Iniciando navegador Firefox")
#     driver = webdriver.Firefox(options=firefox_options)
# else:
#     print("Operación cancelada por el usuario.")
#     exit()

# usar Chrome por defecto, sin interaccion del usuario
driver = webdriver.Chrome(options=chrome_options)

# Abre la página web
link = "https://apphybo.raona.com"
driver.get(link)


def getToken():
    # Da tiempo para que la página se cargue
    # Espera hasta que el elemento con el ID "next" esté presente
    print(f"Cargando página {link}")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "next"))
        )
    except NoSuchElementException:
        print("Botón de inicio de sesión no encontrado.")
        print("Fallo de inicio de sesión ...")
        driver.quit()  # Cerrar el navegador si el elemento no se encuentra
        exit()

    # Inicia sesion
    try:
        # Busca el campo del nombre de usuario y envía los datos
        username_field = driver.find_element(By.ID, "signInName")
        username_field.clear()
        username_field.send_keys(USERNAME_HYBO)
    except NoSuchElementException:
        print("Campo del nombre de usuario no encontrado.")

    try:
        print("Cargando credenciales contraseña ...")
        # Busca el campo de la contraseña y envía los datos
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(PASSWORD_HYBO)
    except NoSuchElementException:
        print("Campo de la contraseña no encontrado.")

    try:
        # Busca el botón de inicio de sesión y haz clic en él
        login_button = driver.find_element(By.ID, "next")
        login_button.click()
        print("Iniciando sesión ...")
    except NoSuchElementException:
        print("Botón de inicio de sesión no encontrado.")
        print("fallo de inicio de sesión ...")

    # Función para verificar si las claves están en localStorage

    def check_keys_in_localstorage(driver, keys):
        script = f"""
        let keysToCheck = {json.dumps(keys)};
        return keysToCheck.every(key => localStorage.getItem(key) !== null);
        """
        return driver.execute_script(script)

    # Lista de claves a verificar en localStorage
    keys_to_check = [
        "39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-accesstoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00-458492eb-f28b-414d-98dd-1bf31a7b453f-https://manageroffice.onmicrosoft.com/api/access_as_user--",
        "39e9e92e-8f46-404d-8014-eb84b2df0d89-b2c_1a_signup_signin_custom.458492eb-f28b-414d-98dd-1bf31a7b453f-manageroffice.b2clogin.com-refreshtoken-53416a92-85aa-4c86-bde0-3c06a7fd8c00----",
    ]

    # Espera hasta que las claves estén en localStorage o se agote el tiempo (15 segundos aquí)
    try:
        print("Extrayendo tokens ...")
        WebDriverWait(driver, 15).until(
            lambda x: check_keys_in_localstorage(driver, keys_to_check)
        )
        print("Datos encontrados en localStorage: ")
    except TimeoutException:
        print(
            "Las claves no se encontraron en localStorage dentro del tiempo especificado."
        )
        driver.quit()
        exit()

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
        print(not_found_message)

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

        # print(f"{credential_type_access}, Secret: {secret_access}\n")
        # print(f"{credential_type_refresh}, Secret: {secret_refresh}\n")

        # Cierra el navegador
        print("Cerrando Navegador")
        driver.quit()

        # Guardar los tokens en archivos separados
        with open("tokenAcceso.txt", "w") as f:
            f.write(secret_access)
        with open("tokenActualizacion.txt", "w") as f:
            f.write(secret_refresh)
        print("Tokens guardados en archivos separados")

        if secret_access is not None:
            return secret_access
        else:
            print("Clave 'secret' no encontrada")
            return None

    except json.JSONDecodeError:
        print("Error al decodificar la cadena JSON")
        # Cierra el navegador
        print("Cerrando Navegador")
        driver.quit()
        return None
    except TypeError:
        print("Tipo de dato incorrecto, se esperaba un diccionario")
        # Cierra el navegador
        print("Cerrando Navegador")
        driver.quit()
        return None
    except Exception as e:
        print(f"Se produjo un error desconocido: {e}")
        # Cierra el navegador
        print("Cerrando Navegador")
        driver.quit()
        return None
