import requests
from dotenv import load_dotenv
import os
import errno
from utils.logger import log, API

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    datos = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=datos)
        response.raise_for_status()
        API.write_log(f'Estado de la respuesta: {response.status_code}')
        API.write_log(f"Mensaje enviado!")
        log("📧")
        return response.json()
    except requests.exceptions.ConnectionError as e:
        # Capturar la excepcion de manera más general y luego verificar el tipo de error
        if e.args and isinstance(e.args[0], requests.packages.urllib3.exceptions.ProtocolError):
            inner_exception = e.args[0].__context__
            if isinstance(inner_exception, ConnectionResetError) and inner_exception.errno == errno.WSAECONNRESET:
                API.write_log(
                    "Peticion denegada por algún firewall, Revisa tu firewall")
            else:
                API.write_log(f"Error de conexión: {e}")
        else:
            API.write_log(f"Error de conexión: {e}")
        return None
    except requests.HTTPError as e:
        API.write_log(f"Error HTTP: {e}, Detalles: {response.text}")
        return None
    except Exception as e:
        API.write_log(f"Error HTTP: {e}, Detalles: {response.text}")
        return None


# # Ejemplo
# send_message(TOKEN, CHAT_ID, "Hola, soy un bot de Telegram")
