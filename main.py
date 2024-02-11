import os
import sys
from getTokensParking import getToken
from getParkingZone import get_parking_place, load_data_place
from getReservedZoneData import extract_information
from sendTelegramMessage import send_message
import time
from dotenv import load_dotenv
from utils.logger import log, API

# Cargando credenciales de acceso
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


if __name__ == "__main__":
    secret_access = getToken()

    # secret_access = "eyJhbGciOiJSUzI1NiIsImtpZCI6InpWVjNyd2hYSlRZRVRnWlczeG9BSnBia0Vienl0T01TWjctS3U2SHZISzAiLCJ0eXAiOiJKV1QifQ.eyJ0aWQiOiIzMDU1ZmE3Zi1hOTQ0LTQ5MjctODAxZS1hNjJiNjMxMTllNDMiLCJuYW1lIjoiSMOpY3RvciBHb256w6FsZXogRGUgbGEgVmVyYSIsImVtYWlsIjoiaGVjdG9yLmdvbnphbGV6QHNlY3VyaXRhc2RpcmVjdC5lcyIsImlkcCI6Im1hbmFnZXJvZmZpY2UiLCJzdWIiOiJmNmFhOGU2My00ZDU1LTRlNmEtYTM3ZS0wYjM4OGEyY2YzODIiLCJPTVRlbmFudElkIjoiN2E5MDNhYzYtYWViNS00Y2Y4LTg3OWMtYzQ4ZjAyZmMzNmU3IiwiT01TdWJzY3JpcHRpb25FbmFibGVkIjp0cnVlLCJPTVN1YnNjcmlwdGlvbkV4cGlyYXRpb25EYXRlIjoxNzQ2MDg2NDAwLCJPTVVzZXJFbmFibGVkIjp0cnVlLCJPTUdyb3VwcyI6ImZmNTBjNzU3LTczYTktNDZiZC05OTFlLTVkYmVlMTIwNDAwYjthODNhYWM4ZC0xNGU5LTQwNzAtYmU3Zi02YmE0NWE4ZjQzN2EiLCJPTVJvbGVzIjoiUGFya2luZ0FwcFVzZXI7Um9vbUFwcFVzZXIiLCJwYXNzd29yZEV4cGlyZWQiOmZhbHNlLCJub25jZSI6IjJjMWI2ZTc3LWZiZjktNDA5YS05MDc0LTMyMmNhNWUzNjA1MSIsInNjcCI6ImFjY2Vzc19hc191c2VyIiwiYXpwIjoiNTM0MTZhOTItODVhYS00Yzg2LWJkZTAtM2MwNmE3ZmQ4YzAwIiwidmVyIjoiMS4wIiwiaWF0IjoxNzA3NjAzMTM2LCJhdWQiOiI2ZDc3NDkzYS0yNGYwLTQ1YmMtYjYxZC0zNDE5YjU5MTAzNWQiLCJleHAiOjE3MDc2MDY3MzYsImlzcyI6Imh0dHBzOi8vbWFuYWdlcm9mZmljZS5iMmNsb2dpbi5jb20vNDU4NDkyZWItZjI4Yi00MTRkLTk4ZGQtMWJmMzFhN2I0NTNmL3YyLjAvIiwibmJmIjoxNzA3NjAzMTM2fQ.KPheLwU1lmwdiXausAXbrP-PZ9H67y1UyYPYVII0hTPkK9zCwfht4OyaKXA2Loa-DjFe7x0Na0e5Hbg0lObMXUAv5Yv2XxIaoB5vulgvxX4tfMKLNpv54cZ5Mk4sjLlXKK4ixVpaXkGC-uPd2-XAA2DY33mKvWZyriwC8G4mdTCtUtMAZdXCR-pDEL7kF3K5PvFHJtH5kj8EyMOyyFDTBeHrXNqxlUoI_3uPwrFyaHuL4UTysFLluiinB54LzqQQN27q7sgBKLuSrxkLgXoWH-wPCT3wnB-FtgLbDLi_6Fr76uO14uVPDcnYHVKscsRGXKvWbXnh4-vcgVpOyAWwfA"

    # if secret_access is not None:
    #     API.write_log("\n__SOLICITANDO PLAZA__")
    #     reservationId = get_parking_place(secret_access)

    #     if reservationId == -1:
    #         msg = "No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duérmete ya!"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if reservationId == -2:
    #         msg = "No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo!!?"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if reservationId == -3:
    #         msg = "<b>Ya existe</b> una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if reservationId == -4:
    #         msg = "Estas excediendo el limite de dias para petición. Máximo 7 días"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if reservationId == -5:
    #         msg = "El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if reservationId is None:
    #         msg = "Error de Servidor, revisa los detalles, y de paso haz algo de provecho y añade esta excepcion en tu bloque except de tu código"
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     API.write_log(f"The reservationId is: {reservationId}")
    #     time.sleep(3)

    #     API.write_log("\n__COMPROBANDO RESERVA DE PLAZA__")
    #     json_data = load_data_place(reservationId, secret_access)

    #     if json_data == -1:
    #         msg = "Plaza no reservada, mala suerte!, prueba otro día o revisa la fecha de solicitud"
    #         API.write_log('Comprueba los datos de la reserva en res/reserved_zone.json')
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     if json_data is None:
    #         msg = "<b>Error</b> al extraer datos de la reserva, verifica el <b>día</b> de la reserva"
    #         API.write_log("Error al extraer datos de la reserva, verifica el dia de la reserva y la hora, recuerda que las reservas se abren a las 08:00 AM")
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)

    #     API.write_log("\n__DATOS DE PLAZA RESERVADA__")
    #     # API.write_log(json_data)

    #     API.write_log("\n__EXTRAYENDO DATOS DE LA PLAZA__")
    #     result = extract_information(json_data)

    #     if result is None:
    #         msg = "Datos de entrada, json_data is None. No se pudo extraer la información. Verifica los datos de entrada."
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)
    #     elif result == -1:
    #         msg = "Datos de entrada, json_data, no es una lista."
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)
    #     elif result == -2:
    #         msg = "Datos de entrada, json_data, es una lista vacia."
    #         API.write_log(msg)
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, msg)
    #         API.write_log("Fin de linea\n")
    #         sys.exit(1)
    #     else:
    #         plaza, zona, turno, matricula, fecha = result
    #         API.write_log(f"Fecha: {fecha}")
    #         API.write_log(f"Zona a aparcar: {zona}")
    #         API.write_log(f"Numero de plaza: {plaza}")
    #         API.write_log(f"Turno: {turno}")
    #         API.write_log(f"Matricula del Vehiculo: {matricula}")
    #         message = "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + "<b>Turno: </b>" + \
    #             turno + "\n" + "<b>Matrícula: </b>" + matricula + "\n" "<b>Fecha: </b>" + fecha
    #         API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
    #         send_message(TOKEN, CHAT_ID, message)
    #         API.write_log("Fin de linea\n")
    # else:
    #     msg = "No se ha obtenido el <b>token</b> correctamente."
    #     send_message(TOKEN, CHAT_ID, msg)
    #     API.write_log("Fin de linea\n")
    #     sys.exit(1)
