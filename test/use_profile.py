from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from dotenv import load_dotenv
import os


load_dotenv()
MICROSOFT_ID = os.getenv("MICROSOFT_ID")
MICROSOFT_PASS = os.getenv("MICROSOFT_PASS")

# Opciones de Firefox
firefox_options = Options()

# # Configuracion de las opciones de Firefox para el modo headless
# firefox_options.add_argument("--headless")
# firefox_options.add_argument("--no-sandbox")
# firefox_options.add_argument("--disable-dev-shm-usage")

# Ruta al perfil de Firefox
profile_path = "/home/christiandavid/.mozilla/firefox/39eehsmk.selenium"
# Cambiar a la ruta del perfil que se utiliza en tu ordenador o copiar dicho perfil en tu maquina de AWS
# Advertencia! El perfil contendra informacion sensible, se debe extremar las precauciones antes de llevarlo a otra maquina
# Se aconseja encriptar el archivo antes de trasferirlo y desencriptarlo en la maquina de AWS

# Crea un objeto FirefoxProfile con la ruta de tu perfil
profile = FirefoxProfile(profile_path)

# Agrega el perfil al objeto de opciones
firefox_options.profile = profile

# Inicializa el driver con las opciones modificadas
driver = webdriver.Firefox(options=firefox_options)


def login_with_firefox_profile():
    try:
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
        print("Error al intentar iniciar sesion con perfil de selenium personalizado:", str(e))


login_with_firefox_profile()

# en windows:
# 1.- Cerrar Firefox: Asegurate de que todas las instancias de Firefox esten cerradas.

# 2.- Abrir el Gestor de Perfiles:
#     Presiona Win + R para abrir el cuadro de dialogo Ejecutar.
#     Escribe firefox.exe -P y presiona Enter. Esto abrira el Gestor de Perfiles.

# 3.- Crea el Perfil:
# Haz clic en el boton "Crear perfil" en el gestor de perfiles que se abre. Esto iniciara el asistente de creacion de perfiles.
# Haz clic en "Siguiente" en el asistente.
# Elije un nombre y dale a siguiente. Puedes dejar que Firefox elija una ubicacion predeterminada o puedes especificar una ruta de directorio personalizada.
# Antes de darle a finalizar asegurate de copiar la ruta del perfil de Firefox en la variable profile_path de este script.

# Nota: La ventaja de utilizar este metodo es que no necesitas crear un nuevo usuario cada vez que quieres probar algo.
# Si todo sale bien, deberias estar logueado en la aplicacion sin necesidad de ingresar tus credenciales cada vez que inicies Selenium.
# Si hay algun problema, puedes volver a intentarlo con otro perfil de Firefox.
