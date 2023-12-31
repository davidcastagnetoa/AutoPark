import os
# # FOR TEST
# Imprimir todas las variables de entorno
# for key, value in os.environ.items():
#     print(f"{key}: {value}")

import sys
from getTokensParking import getToken
from getParkingZone import get_parking_place, load_data_place
from getReservedZoneData import extract_information
from sendTelegramMessage import send_message
import time
from dotenv import load_dotenv


# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if __name__ == "__main__":
    secret_access = getToken()
    if secret_access is not None:
        print("\n__SOLICITANDO PLAZA__")
        reservationId = get_parking_place(secret_access)

        if reservationId == -1:
            msg = "No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duermete ya!"
            send_message(TOKEN, CHAT_ID, msg)
            sys.exit(1)

        if reservationId == -2:
            msg = "No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo?"
            send_message(TOKEN, CHAT_ID, msg)
            sys.exit(1)

        if reservationId == -3:
            msg = "<b>Ya existe</b> una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
            send_message(TOKEN, CHAT_ID, msg)
            sys.exit(1)

        if reservationId is None:
            msg = "Error de Servidor, revisa los detalles, y de paso haz algo de provecho y añade esta excepcion en tu bloque except de tu codigo"
            print(msg)
            send_message(TOKEN, CHAT_ID, msg)
            sys.exit(1)

        print("The reservationId is:", reservationId)
        time.sleep(2)
        print("\n__EXTRAYENDO DATOS DE LA PLAZA__")
        json_data = load_data_place(reservationId, secret_access)

        if json_data is None:
            msg = "<b>Error</b> al extraer datos de la reserva, verifica el <b>dia</b> de la reserva"
            print("Error al extraer datos de la reserva, verifica el dia de la reserva")
            send_message(TOKEN, CHAT_ID, msg)
            sys.exit(1)

        print("\n__DATOS DE PLAZA RESERVADA__")
        plaza, zona, turno, matricula, fecha = extract_information(
            json_data)
        print(f"Fecha: {fecha}")
        print(f"Zona a aparcar: {zona}")
        print(f"Numero de plaza: {plaza}")
        print(f"Turno: {turno}")
        print(f"Matricula del Vehiculo: {matricula}")
        message = "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + "<b>Turno: </b>" + \
            turno + "\n" + "<b>Matrícula: </b>" + matricula + "\n" "<b>Fecha: </b>" + fecha

        print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
        send_message(TOKEN, CHAT_ID, message)
    else:
        msg = "No se ha obtenido el <b>token</b> correctamente."
        send_message(TOKEN, CHAT_ID, msg)
        sys.exit(1)
