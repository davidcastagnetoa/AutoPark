import os
import sys
from getTokensParking import getToken
from getParkingZone import get_parking_place, load_data_place
from getReservedZoneData import extract_information
from sendTelegramMessage import send_message
import time
from dotenv import load_dotenv
from utils.logger import log, API
from halo import Halo

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


if __name__ == "__main__":
    secret_access = getToken()
    API.write_log("Aplicando tiempo de espera, enviando token de 365 a DB de Hybo...")
    spinner = Halo(text='Solicitud de token iniciada', spinner='dots')
    spinner.start()
    spinner.text = "Aplicando tiempo de espera, enviando token de 365 a DB de Hybo..."
    time.sleep(35)

    # secret_access = ""

    if secret_access is not None:
        API.write_log("\n__SOLICITANDO PLAZA__")
        print("\n__SOLICITANDO PLAZA__")
        spinner.text = "Ejecutando funcion de reserva de plaza"
        reservationId = get_parking_place(secret_access)

        if reservationId == -1:
            msg = "No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duermete ya!"
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId == -2:
            msg = "No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo!!?"
            spinner.fail("No es posible seleccionar plaza los fines de semana. Que cojones piensas hacer un finde en el trabajo!?")
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId == -3:
            msg = "<b>Ya existe</b> una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
            spinner.fail("Ya existe una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador")
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId == -4:
            msg = "Estas excediendo el limite de dias para peticion. Maximo 7 dias"
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId == -5:
            msg = "El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId is None:
            msg = "Error de Servidor, revisa los detalles, y de paso haz algo de provecho y añade esta excepcion en tu bloque except de tu codigo"
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")    
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        API.write_log(f"The reservationId is: {reservationId}")
        API.write_log("Aplicando tiempo de espera para validacion de token en la DB de Hybo.")
        time.sleep(10)

        API.write_log("\n__COMPROBANDO RESERVA DE PLAZA__")
        print("\n__COMPROBANDO RESERVA DE PLAZA__")
        spinner.text = "Comprobando pase de reserva"
        json_data = load_data_place(reservationId, secret_access)

        if json_data == -1:
            msg = "Plaza no reservada, mala suerte!, prueba otro dia o revisa la fecha de solicitud"
            API.write_log('Comprueba los datos de la reserva en res/reserved_zone.json')
            API.write_log(msg)
            spinner.fail(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if json_data is None:
            msg = "<b>Error</b> al extraer datos de la reserva, verifica el <b>dia</b> de la reserva"
            spinner.fail("Error al extraer datos de la reserva, verifica el dia de la reserva")
            API.write_log("Error al extraer datos de la reserva, verifica el dia de la reserva y la hora, recuerda que las reservas se abren a las 08:00 AM")
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        API.write_log("\n__DATOS DE PLAZA RESERVADA__")
        print("\n__DATOS DE PLAZA RESERVADA__")
        # API.write_log(json_data)
        spinner.succeed("Pase de reserva comprobado!")

        API.write_log("\n__EXTRAYENDO DATOS DE LA PLAZA__")
        print("\n__EXTRAYENDO DATOS DE LA PLAZA__")
        result = extract_information(json_data)
        spinner.text = "Extrayendo datos de plaza reservada"

        if result is None:
            msg = "Datos de entrada, json_data is None. No se pudo extraer la informacion. Verifica los datos de entrada."
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        elif result == -1:
            msg = "Datos de entrada, json_data, no es una lista."
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        elif result == -2:
            msg = "Datos de entrada, json_data, es una lista vacia."
            spinner.fail(msg)
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        else:
            spinner.succeed("Datos de plaza extraido!")
            plaza, zona, turno, matricula, fecha = result
            API.write_log(f"Fecha: {fecha}")
            API.write_log(f"Zona a aparcar: {zona}")
            API.write_log(f"Numero de plaza: {plaza}")
            API.write_log(f"Turno: {turno}")
            API.write_log(f"Matricula del Vehiculo: {matricula}")
            message = "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + "<b>Turno: </b>" + \
                turno + "\n" + "<b>Matricula: </b>" + matricula + "\n" "<b>Fecha: </b>" + fecha
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, message)
            API.write_log("Fin de linea\n")
    else:
        msg = "No se ha obtenido el <b>token</b> correctamente."
        send_message(TOKEN, CHAT_ID, msg)
        spinner.fail("No se ha obtenido el token correctamente!")
        API.write_log("Fin de linea\n")
        print("Fin de linea\n")
        sys.exit(1)
