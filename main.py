import os
import sys
from datetime import datetime, timedelta
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

# Otras variables
segundo_intento = False
debug_mode = True  # Cambia a True para activar modo debug

# Función para calcular el tiempo de espera hasta las 07:59:30


def calcular_tiempo_espera(h, m, s, ms):
    ahora = datetime.now()
    objetivo = ahora.replace(hour=h, minute=m, second=s, microsecond=ms)
    if ahora > objetivo:
        objetivo += timedelta(days=1)  # Si ya pasó la hora, espera hasta el día siguiente
    tiempo_espera = (objetivo - ahora).total_seconds()
    return tiempo_espera


if __name__ == "__main__":
    API.write_log("\n__CONSULTA DE TOKEN__")
    print("\n__CONSULTA DE TOKEN__")
    secret_access = getToken()
    spinner = Halo(text='Solicitud de token iniciada', spinner='dots')
    spinner.start()
    if secret_access == -1:
        log = "Primer intento de token fallido. Fallo al obtener datos en LocalStorage."
        API.write_log("Primer intento de token fallido. Fallo al obtener datos en LocalStorage. Se realiza segundo intento.")
        spinner.fail(log)
        spinner.text = 'Lanzando segundo intento'
        time.sleep(10)
        secret_access = getToken()

    if secret_access is not None:
        spinner.text = 'A la espera de la hora acordada'
        tiempo_espera = calcular_tiempo_espera(8, 00, 00, 00)
        ahora = datetime.now().strftime("%H:%M:%S")
        API.write_log("\n__SOLICITUD DE PLAZA__")
        print("\n__SOLICITUD DE PLAZA__")
        spinner.text = f'Solicitando plaza a las {ahora}'
        API.write_log(f'Solicitando plaza a las {ahora}')
        API.write_log(f'Tiempo de espera en segundos hasta las 08:00: {tiempo_espera}')

        if debug_mode == False:
            if (tiempo_espera) > 700:
                log = f'Tiempo de espera excedido. Cancelando peticion, Hay que solicitar el token antes de las {ahora}. Cambia la hora de solicitud en crontab.'
                msg = f'Tiempo de espera excedido. <b>Cancelando peticion</b>, Hay que solicitar el token antes de las {ahora}. Cambia la hora de solicitud en <b>crontab</b>.En caso de duda consulta con el <b>Gran Administrador XD</b>'
                spinner.fail(log)
                API.write_log(log)
                send_message(TOKEN, CHAT_ID, msg)
                sys.exit(1)

            spinner.text = f"Esperando {tiempo_espera} segundos hasta las 08:00:00"
            time.sleep(tiempo_espera)  # Espera hasta las 08:00:00

        spinner.text = "Ejecutando funcion de reserva de plaza"
        reservationId = get_parking_place(secret_access, use_zone_2=False)

        if reservationId in [-1, -2, -3, -4, -5, -6, None]:
            if reservationId == -1:
                msg = "Pase de reservada NO OBTENIDO. No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duérmete ya!"
                log = "Pase de reservada NO OBTENIDO. No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duérmete ya!"
            elif reservationId == -2:
                msg = "Pase de reservada NO OBTENIDO. No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo!!?"
                msg = "Pase de reservada NO OBTENIDO. No es posible seleccionar plaza los fines de semana. Que cojones piensas hacer un finde en el trabajo!!?"
            elif reservationId == -3:
                msg = "Pase de reservada NO OBTENIDO. <b>Ya existe</b> una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
                log = "Pase de reservada NO OBTENIDO. Ya existe una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
            elif reservationId == -4:
                msg = "Pase de reservada NO OBTENIDO. Estas excediendo el limite de dias para petición. Máximo 7 días"
                log = "Pase de reservada NO OBTENIDO. Estas excediendo el limite de dias para petición. Máximo 7 días"
            elif reservationId == -5:
                msg = "Pase de reservada NO OBTENIDO. El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
                log = "Pase de reservada NO OBTENIDO. El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
            else:
                msg = "Pase de reservada NO OBTENIDO. <b>Error</b> al extraer datos de la reserva, verifica el <b>día</b> de la reserva"
                log = "Pase de reservada NO OBTENIDO. Error al extraer datos de la reserva, verifica el día de la reserva"

            API.write_log(log)
            spinner.fail(log)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        if reservationId == -6:
            segundo_intento = True
            msg = "Pase de reservada NO OBTENIDO. El servidor rechaza la peticion. Servidor de origen no se está comunicando con el servidor de enlace. Repitiendo solicitud a MD en 30 segundos en Priegola"
            API.write_log(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Iniciando segundo intento en 30 segundos")

            time.sleep(30)

            reservationId = get_parking_place(secret_access, use_zone_2=True)  # Aqui solicitamos a Priegola
            if reservationId in [-1, -2, -3, -4, -5, -6, None]:
                if reservationId == -1:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duérmete ya!"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. No es posible reservar entre las 0:00 y 8:00 horas. Deja ya de hacer pruebas y duérmete ya!"
                elif reservationId == -2:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo!!?"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. No es posible seleccionar plaza los <b>fines de semana</b>. Que cojones piensas hacer un finde en el trabajo!!?"
                elif reservationId == -3:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. <b>Ya existe</b> una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. Ya existe una plaza reservada!, revisa los mensajes previos o consulta la aplicacion web en un navegador"
                elif reservationId == -4:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. Estas excediendo el limite de dias para petición. Máximo 7 días"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. Estas excediendo el limite de dias para petición. Máximo 7 días"
                elif reservationId == -5:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. El servidor rechaza la peticion. El token usado no es valido. Realiza pruebas en postman para verificar la validez del token"
                elif reservationId == -6:
                    msg = "<b>Error</b> al solicitar la reserva. Pase de reservada NO OBTENIDO. Error Bad Gateway. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento. <b>Vamos que te estan puteando, pero no te rindas!</b>"
                    log = "Error al solicitar la reserva. Pase de reservada NO OBTENIDO. Error Bad Gateway. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                else:
                    msg = "Segundo intento fallido. Pase de reservada NO OBTENIDO. Error de Servidor, revisa los detalles, y de paso haz algo de provecho y añade esta excepcion en tu bloque except de tu código"
                    log = "Segundo intento fallido. Pase de reservada NO OBTENIDO. Error de Servidor, revisa los detalles, y de paso haz algo de provecho y añade esta excepcion en tu bloque except de tu código"

                spinner.fail(log)
                API.write_log(log)
                print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                send_message(TOKEN, CHAT_ID, msg)
                API.write_log("Fin de linea\n")
                sys.exit(1)

        API.write_log(f"The reservationId is: {reservationId}")
        API.write_log(f"The reservationId is: {reservationId}")
        time.sleep(3)

        API.write_log("\n__COMPROBANDO RESERVA DE PLAZA__")
        print("\n__COMPROBANDO RESERVA DE PLAZA__")

        if segundo_intento == False:
            spinner.text = "Comprobando pase de reserva en Victoria"
            API.write_log("Comprobando pase de reserva en Victoria")
            json_data = load_data_place(reservationId, secret_access, use_zone_2=False)
        else:
            spinner.text = "Comprobando pase de reserva en Priegola"
            API.write_log("Comprobando pase de reserva en Priegola")
            json_data = load_data_place(reservationId, secret_access, use_zone_2=True)

        if json_data in [-1, -2, -4]:
            if json_data == -1:
                msg = "<b>Peticion aprobada</b>, pero la respuesta del servidor <b>no es un JSON valido</b>. Comprueba en pagina web la reserva"
                log = f"La Peticion fue aprobada, pero no se pudo comprobar la reserva con el id: {reservationId}. La respuesta del servidor no es un JSON valido. Comprueba en pagina web la reserva"
            elif json_data == -2:
                msg = "<b>Error</b> al extraer datos de la reserva. El middleware rechaza la peticion. <b>El token usado no es valido</b>. verifica en la pagina de Hybo"
                log = "Error al extraer datos de la reserva. El middleware rechaza la peticion. El token usado no es valido. verifica en la pagina de Hybo"
            else:
                msg = "<b>Error</b> al extraer datos de la reserva. Plaza no reservada, mala suerte!, prueba otro día o revisa la fecha de solicitud."
                log = "Error al extraer datos de la reserva. Plaza no reservada, mala suerte!, prueba otro día o revisa la fecha de solicitud."

            API.write_log(log)
            spinner.fail(log)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)

        elif json_data in [-3, -5, None]:
            if json_data == -3:
                msg = "<b>Error</b> al extraer datos de la reserva. El middleware rechaza la peticion, recibió una respuesta inválida de un servidor upstream. <b>Error 502</b>. Repitiendo solicitud a MD en 30 segundos"
                log = "Error al extraer datos de la reserva. El middleware rechaza la peticion, recibió una respuesta inválida de un servidor upstream. <b>Error 502</b>. Repitiendo solicitud a MD en 30 segundos"
            elif json_data == -5:
                msg = "<b>Error</b> al extraer datos de la reserva. middleware rechaza la peticion. Error PETICION HTTP Desconociodo. Mapea el error. Repitiendo solicitud a MD en 30 segundos"
                log = "Error al extraer datos de la reserva. middleware rechaza la peticion. Error PETICION HTTP Desconociodo. Mapea el error. Repitiendo solicitud a MD en 30 segundos"
            else:
                msg = "<b>Error</b> al extraer datos de la reserva. El middleware rechaza la peticion. Error Desconocido. Mapea el error que ha devuelto el servidor. Repitiendo solicitud a MD en 30 segundos"
                log = "Error al extraer datos de la reserva. El middleware rechaza la peticion, recibió una respuesta inválida de un servidor upstream. <b>Error 502</b>. Repitiendo solicitud a MD en 30 segundos"

            API.write_log(log)
            spinner.fail(log)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            time.sleep(30)

            if segundo_intento == False:
                spinner.text = "Segundo intento. Comprobando pase de reserva en Victoria"
                API.write_log("Segundo intento. Comprobando pase de reserva en Victoria")
                json_data = load_data_place(reservationId, secret_access, use_zone_2=False)
            else:
                spinner.text = "Segundo intento. Comprobando pase de reserva en Priegola"
                API.write_log("Segundo intento. Comprobando pase de reserva en Priegola")
                json_data = load_data_place(reservationId, secret_access, use_zone_2=True)

            if json_data in [-1, -2, -3, -4, -5, None]:
                if json_data == -1:
                    msg = "Segundo intento fallido. <b>Peticion aprobada</b>, pero la respuesta del servidor <b>no es un JSON valido</b>. Comprueba en pagina web la reserva"
                    log = "Segundo intento fallido. Peticion aprobada, pero la respuesta del servidor no es un JSON valido. Comprueba en pagina web la reserva"
                elif json_data == -2:
                    msg = "Segundo intento fallido. <b>Error</b> al extraer datos de la reserva. El middleware rechaza la peticion. <b>El token usado no es valido</b>. verifica en la pagina de Hybo"
                    log = "Segundo intento fallido. Error al extraer datos de la reserva. El middleware rechaza la peticion. El token usado no es valido. verifica en la pagina de Hybo"
                elif json_data == -3:
                    msg = "<b>Error</b> al extraer datos de la reserva. El middleware rechaza la peticion, recibió una respuesta inválida de un servidor upstream. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                    log = "Error al extraer datos de la reserva. El middleware rechaza la peticion, recibió una respuesta inválida de un servidor upstream. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                elif json_data == -4:
                    msg = "<b>Error</b> al extraer datos de la reserva. Plaza no reservada, mala suerte!, prueba otro día o revisa la fecha de solicitud."
                    log = "Error al extraer datos de la reserva. Plaza no reservada, mala suerte!, prueba otro día o revisa la fecha de solicitud."
                elif json_data == -5:
                    msg = "<b>Error</b> al extraer datos de la reserva. middleware rechaza la peticion. Error PETICION HTTP Desconociodo. Mapea el error. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                    log = "Error al extraer datos de la reserva. middleware rechaza la peticion. Error PETICION HTTP Desconociodo. Mapea el error. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                else:
                    msg = "Segundo intento fallido. <b>Error</b>. El middleware rechaza la peticion. Error Desconocido. Mapea el error que ha devuelto el servidor. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."
                    log = "Segundo intento fallido. Error!. El middleware rechaza la peticion. Error Desconocido. Mapea el error que ha devuelto el servidor. Se han realizado dos intentos en 30 segundos de diferencia. Valora aumentar el tiempo o añadir un tercer intento."

                spinner.fail(log)
                API.write_log(log)
                print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
                API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
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
        spinner.text = "Extrayendo datos de plaza reservada, guardando en reservas.db"

        if result is None:
            msg = "Datos de entrada, json_data is None. No se pudo extraer la información. Verifica los datos de entrada."
            API.write_log(msg)
            spinner.fail(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        elif result == -1:
            msg = "Datos de entrada, json_data, no es una lista."
            API.write_log(msg)
            spinner.fail(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        elif result == -2:
            msg = "Datos de entrada, json_data, es una lista vacia."
            API.write_log(msg)
            spinner.fail(msg)
            API.write_log("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            print("\n__ENVIANDO MENSAJE POR TELEGRAM__")
            send_message(TOKEN, CHAT_ID, msg)
            API.write_log("Fin de linea\n")
            sys.exit(1)
        else:
            spinner.succeed("Datos de plaza extraído!")
            plaza, zona, turno, matricula, fecha, id = result

            API.write_log(f"Id: {id}")
            API.write_log(f"Fecha: {fecha}")
            API.write_log(f"Zona a aparcar: {zona}")
            API.write_log(f"Numero de plaza: {plaza}")
            API.write_log(f"Turno: {turno}")
            API.write_log(f"Matricula del Vehiculo: {matricula}")
            message = "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + "<b>Turno: </b>" + \
                turno + "\n" + "<b>Matrícula: </b>" + matricula + "\n" "<b>Fecha: </b>" + fecha
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
