import requests
from dotenv import load_dotenv
import os
import errno
from halo import Halo
from flask import Flask, request, jsonify
from sendTelegramMessage import send_message
from deleteParkingZone import delete_parking_place
from getTokensParking import getToken
from utils.logger import log, API
from halo import Halo

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Llamando spinner
spinner = Halo(text='Comprobando variables de entorno', spinner='dots')
spinner.start()


# Obteniendo Token
secret_access = getToken()
if secret_access is not None:
    API.write_log("\n__SOLICITANDO TOKEN DE ACCESO__")
    print("\n__SOLICITANDO TOKEN DE ACCESO__")
    spinner.text = "Llamando a funcion para obtener reservationId"
    reservationId = ""


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    update = request.get_json()
    print("Received webhook:", update)

    # Procesar el comando /hello
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text == '/hello':
            send_message(TOKEN, CHAT_ID, "Hola, he recibido tu saludo y te respondo. soy un bot de Telegram")
            # Aquí puedes añadir más lógica, como responder al mensaje
            if text == '/delete':
                pass
                # delete_parking_place(secret_access, reservationId)

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run()
