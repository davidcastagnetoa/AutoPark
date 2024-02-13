import requests
from dotenv import load_dotenv
import os
from utils.logger import log, API
from halo import Halo

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(token, chat_id, message):
    spinner = Halo(text='Preparando envío de mensaje', spinner='dots')
    spinner.start()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    datos = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    spinner.text = "Enviando mensaje"
    try:
        response = requests.post(url, data=datos)
        response.raise_for_status()
        API.write_log(f'Estado de la respuesta: {response.status_code}')
        API.write_log("Mensaje enviado!")
        spinner.succeed("Mensaje enviado!")
        return response.json()
    except requests.ConnectionError as e:
        # Directamente capturamos ConnectionResetError desde la excepción de ConnectionError
        if 'Connection aborted.' in str(e) and (
                'Connection reset by peer' in str(e) or 'Se ha forzado la interrupción de una conexión existente por el host remoto' in str(e)):
            custom_message = "Conexion interrumpida: parece que una politica de seguridad ha forzado la interrupcion de esta conexion. Esto puede deberse a restricciones impuestas por un firewall o configuraciones de seguridad en el servidor o la red local. Consulte con el administrador de su red para obtener mas detalles y posibles soluciones."
            API.write_log(custom_message)
            spinner.fail("Fallo de envio de mensaje, denegado por Firewall ")
        else:
            API.write_log(f"Error de conexión no especifico: {e}")
            spinner.fail(f"Error de conexión no especifico: {e}")
        return None
    except Exception as e:
        API.write_log(f"Error desconocido: {e}")
        spinner.fail("Fallo al enviar mensaje")
        return None


# Ejemplo de uso
send_message(TOKEN, CHAT_ID, "Hola, soy un bot de Telegram")
