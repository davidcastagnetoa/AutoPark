import requests
from dotenv import load_dotenv
import os
import errno
from datetime import datetime
from halo import Halo
from flask import Flask, request, jsonify
from sendTelegramMessage import send_message
from deleteParkingZone import delete_parking_place
from getTokensParking import getToken
from deleteParkingZone import reservedPlaceData
from utils.logger import log, API
from halo import Halo

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Llamando spinner
spinner = Halo(text='Comprobando variables de entorno de telegram', spinner='dots')

app = Flask(__name__)

# Estado de la conversación por chat_id
conversation_state = {}


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    update = request.get_json()
    chat_id = update['message']['chat']['id']
    print("Received webhook:", update)
    spinner.start()
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text == '/hello':
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, "Hola, he recibido tu saludo y te respondo. soy un bot de Telegram")

        if text == '/delete':
            conversation_state[chat_id] = 'awaiting_date'
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, "Escribe la fecha de la reserva a eliminar en formato YYYY-MM-DD, o escribe el comando <b>cancel</b> para cancelar.")

        elif text == '/cancel' and conversation_state.get(chat_id) == 'awaiting_date':
            conversation_state.pop(chat_id, None)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, "Operación cancelada.")

        elif conversation_state.get(chat_id) == 'awaiting_date':
            # Aquí procesarías la fecha enviada por el usuario
            conversation_state.pop(chat_id, None)

            spinner.text = "Validando fecha"
            try:
                date_to_delete = datetime.strptime(text, "%Y-%m-%d")
                # Procesa la fecha si es válida.
                spinner.succeed(f"Fecha válida recibida: {date_to_delete}")
                # Aquí continuarías con la lógica para eliminar la reserva...

                API.write_log("\n__SOLICITANDO TOKEN DE ACCESO__")
                print("\n__SOLICITANDO TOKEN DE ACCESO__")

                spinner.text = "Solicitando token"
                try:
                    secret_access = getToken()
                    # secret_access = "faketoken0123456789jdt"
                    if secret_access is not None:
                        spinner.succeed("Token Obtenido")
                        API.write_log("Token Obtenido")

                        spinner.text = "Solicitando fecha de la plaza a liberar"

                        if text == '/cancel' and conversation_state.get(chat_id) == 'awaiting_date':
                            conversation_state.pop(chat_id, None)
                            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                            send_message(TOKEN, CHAT_ID, "Operación cancelada.")

                        spinner.text = "Obteniendo información de la plaza"
                        reservedID, plaza, zona, turno, matricula, fecha = reservedPlaceData(date_to_delete)

                        if reservedID is not None:
                            spinner.succeed("Información de la plaza obtenida")
                            spinner.succeed(f"Id de la plaza obtenido: {reservedID}")
                            API.write_log(f"Información de la plaza obtenida. Id de la plaza obtenido: {reservedID}")
                            spinner.text = "Eliminando plaza..."
                            try:
                                result_Delete_Place = delete_parking_place(secret_access, reservedID)

                                if result_Delete_Place == -5:
                                    msg = "El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
                                    spinner.fail(msg)
                                    API.write_log(msg)
                                    API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    send_message(TOKEN, CHAT_ID, msg)
                                    raise Exception(msg)

                                if result_Delete_Place == -6:
                                    msg = "La plaza de garaje especificada no existe o ya fue eliminada"
                                    spinner.fail(msg)
                                    API.write_log(msg)
                                    API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    send_message(TOKEN, CHAT_ID, msg)
                                    raise Exception(msg)

                                if result_Delete_Place is not True:
                                    msg = "El servidor rechaza la peticion. Revisa los errores"
                                    spinner.fail(msg)
                                    API.write_log(msg)
                                    API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    send_message(TOKEN, CHAT_ID, msg)
                                    raise Exception(msg)

                                else:
                                    spinner.succeed("Plaza eliminada!")
                                    API.write_log("Plaza eliminada!")

                                    message = "<b>Plaza Eliminada</b>\n" + "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + \
                                        "<b>Turno: </b>" + turno + "\n" + "<b>Matrícula: </b>" + matricula + "\n" + "<b>Fecha: </b>" + fecha

                                    API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                                    send_message(TOKEN, CHAT_ID, message)

                            except Exception as e:
                                spinner.fail("Error al eliminar la plaza")
                                spinner.fail(f"Fallo de funcion delete_parking_place: {str(e)}")
                                API.write_log(f"Error al eliminar la plaza. Fallo de funcion delete_parking_place: {str(e)}")
                                raise Exception(f"Error al eliminar la plaza, . No es posible eliminar la plaza")
                        else:
                            spinner.fail("No se ha obtenido la información de la plaza")
                            spinner.fail("Plaza no reservada o fecha incorrecta")
                            API.write_log("No se ha obtenido la información de la plaza. No se pudo obtener el ID de la reserva.")
                            raise Exception("No existe plaza reservada para esa fecha. Plaza <b>no</b> reservada o fecha incorrecta")
                    else:
                        spinner.fail("No se ha obtenido el token correctamente.")
                        API.write_log("No se ha obtenido el token correctamente.")
                        raise Exception("No se ha obtenido el <b>token</b> correctamente. No es posible eliminar la plaza")

                    spinner.stop()

                except Exception as e:
                    msg = f"{str(e)}"
                    spinner.fail(msg)
                    API.write_log(msg)
                    API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                    print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                    send_message(TOKEN, CHAT_ID, msg)
                    spinner.stop()
                    API.write_log("Fin de linea\n")

                    return jsonify({
                        "status": "failed",
                        "msg": msg
                    })

            except ValueError:
                # Si falla la conversión, envía un mensaje de error
                spinner.fail("Formato de fecha incorrecto. Por favor, usa el formato YYYY-MM-DD.")
                API.write_log("Formato de fecha incorrecto. Por favor, usa el formato YYYY-MM-DD.")
                API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                send_message(TOKEN, CHAT_ID, "Formato de fecha incorrecto. Por favor, usa el formato YYYY-MM-DD.")

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run()
