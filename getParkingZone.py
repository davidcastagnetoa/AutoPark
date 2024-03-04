import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils.logger import log, API
from halo import Halo

from getReservedZoneData import extract_information

# Cargando credenciales de acceso
load_dotenv()
URL = os.getenv("URL")

# Accede a la variable en formato JSON
json_data = os.getenv("JSON_DATA")

# Llamando spinner
spinner = Halo(text='Comprobando variables de entorno', spinner='dots')
spinner.start()

if json_data:
    config = json.loads(json_data)
    # Aqui puedes definir la zona en la que se quiere reservar plaza
    ZONE = config["zone_victoria_2"]
    ZONE_2 = config["zone_priegola_2"]
    PLATE = config["plate"]
    USERID = config["userId"]
    OFFICEID = config["officeId"]
    VEHICLEID = config["vehicleId"]
    DATETIMEVEHICLE_CREATED = config["createdAtUtc"]
    DATETIMEVEHICLE_MODIFIED = config["modifiedAtUtc"]
    TURN = config["turn"]
    # Acceder a otros valores en 'config' según sea necesario
    spinner.succeed("Variables de entorno encontradas")
else:
    API.write_log("No se encontro la configuracion JSON.")
    spinner.fail("No se encontro la configuracion JSON.")

# La fecha es 7 días después de hoy
date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

# # La fecha actual
# date = datetime.now().strftime("%Y-%m-%d")

API.write_log(f"Fecha a solicitar plaza: {date}")
print(f"Fecha a solicitar plaza: {date}")


# Reservar la plaza y Obtener su ID
def get_parking_place(secret, use_zone_2=False):
    # URL del endpoint
    url = URL + "/BookingsByContext"

    # Victoria en el primer intento, sino Priegola
    zone_to_use = ZONE_2 if use_zone_2 else ZONE

    # Construyendo los datos para la peticion
    headers = {
        "Authorization": "Bearer " + secret,
        "Content-Type": "application/json; charset=utf-8",
    }

    # Datos a enviar en el payload
    payload = {
        "userId": USERID,
        "officeId": OFFICEID,
        "zoneId": zone_to_use,
        "vehicle": {
            "id": VEHICLEID,
            "objectType": "OM.Vehicle",
            "schemaVersion": 0.1,
            "createdBy": "OM.Api",
            "createdAtUtc": DATETIMEVEHICLE_CREATED,
            "modifiedBy": "OM.Api",
            "modifiedAtUtc": DATETIMEVEHICLE_MODIFIED,
            "type": "Car",
            "engine": "Fuel",
            "licensePlate": PLATE,
        },
        "bookingType": "Day",
        "turn": TURN,
        "date": date,
        "seatId": [],
        "isGroupReservation": False,
        "isCarSharing": False,
    }

    reservationId = None

    if secret:
        # Realizar la peticion POST
        spinner.text = "Obteniendo Pase de reserva."
        try:
            API.write_log("Obteniendo Pase de reserva...")
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Verificar el estado de la respuesta
            response.raise_for_status()

            API.write_log(f"Estado de respuesta para obtener pase de reserva : {response.status_code}")
            # API.write_log(
            #     f"Texto de respuesta para obtener pase de reserva : {response.text}")

            API.write_log("Pase de reserva adquirido!!!")
            spinner.succeed("Pase de reserva adquirido!!!")

            # La respuesta es una cadena de texto con los valores separados por |
            # Elimina espacios en blanco al inicio y al final
            response_text = (response.text.strip())
            values = response_text.split("|")

            # Asignar los valores a las variables correspondientes
            if len(values) >= 3:
                tenantId = values[0].strip('"')
                zoneId = values[1].strip('"')
                reservationId = values[2].strip('"')

                # Imprimir o usar las variables según sea necesario
                API.write_log("Extrayendo variables id del Pase de reserva...")
                API.write_log(f"Tenant ID: {tenantId}")
                API.write_log(f"Zone ID: {zoneId}")
                API.write_log(f"Reservation ID: {reservationId}")
                API.write_log(f"Reservation Date: {date}")

                # Solo usaremos la ultima que es el ID de la plaza encontrada
                spinner.succeed("ID de plaza encontrado")

                return reservationId
            else:
                API.write_log("Error al reservar la plaza, La respuesta no contiene los 3 valores. Pase de reserva NO adquirido!")
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400 and '409-11' in response.text:
                API.write_log(f"No es posible reservar entre las 0:00 y 8:00 horas, Detalles: {response.text}")
                spinner.fail(f"No es posible reservar entre las 0:00 y 8:00 horas, Detalles: {response.text}")
                return -1
            elif response.status_code == 400 and 'It is not possible to select the weekend.' in response.text:
                API.write_log(f"Error HTTP: 400 - No es posible seleccionar el fin de semana, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: 400 - No es posible seleccionar el fin de semana, Detalles: {response.text}")
                return -2
            elif response.status_code == 409 and '409-12' in response.text:
                API.write_log(f"Error HTTP: 409 - Ya existe una plaza reservada a esta fecha, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: 409 - Ya existe una plaza reservada a esta fecha, Detalles: {response.text}")
                return -3
            elif response.status_code == 400 and 'Booking max days exceeded' in response.text:
                API.write_log(f"Error HTTP: 400 - Estas excediendo el limite de dias para peticion, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: 400 - Estas excediendo el limite de dias para peticion, Detalles: {response.text}")
                return -4
            elif response.status_code == 401:
                API.write_log(f"Error HTTP: 401, El servidor rechaza la peticion. El token usado no es valido, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: 401, El servidor rechaza la peticion. El token usado no es valido, Detalles: {response.text}")
                return -5
            elif response.status_code == 502:
                API.write_log(f"Error HTTP: 502, Bad Gateway, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: 502, Bad Gateway, Detalles: {response.text}")
                return -6
            else:
                API.write_log(f"Error HTTP: {http_err}, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: {http_err}, Detalles: {response.text}")
                return None
        except requests.exceptions.ConnectionError as conn_err:
            API.write_log(f"Error de conexion: {conn_err}, Detalles: {response.text}")
            spinner.fail(f"Error de conexion: {conn_err}, Detalles: {response.text}")
        except requests.exceptions.Timeout as timeout_err:
            API.write_log(f"Error de timeout: {timeout_err}, Detalles: {response.text}")
            spinner.fail(f"Error de timeout: {timeout_err}, Detalles: {response.text}")
        except requests.exceptions.RequestException as req_err:
            API.write_log(f"Error general en la peticion: {req_err}, Detalles: {response.text}")
            spinner.fail(f"Error general en la peticion: {req_err}, Detalles: {response.text}")

    else:
        API.write_log("Se requiere el token para realizar la solicitud")
        spinner.fail("Se requiere el token para realizar la solicitud")
        return None


def load_data_place(reservation_id, secret, use_zone_2=False):
    zone_to_use = ZONE_2 if use_zone_2 else ZONE
    # Construyendo los datos para la peticion
    headers = {
        "Authorization": "Bearer " + secret,
        "Content-Type": "application/json; charset=utf-8",
    }
    # Datos a enviar en el payload
    body = {
        "userId": USERID,
        "officeId": OFFICEID,
        "zoneId": zone_to_use,
        "vehicle": {
            "id": VEHICLEID,
            "objectType": "OM.Vehicle",
            "schemaVersion": 0.1,
            "createdBy": "OM.Api",
            "createdAtUtc": DATETIMEVEHICLE_CREATED,
            "modifiedBy": "OM.Api",
            "modifiedAtUtc": DATETIMEVEHICLE_MODIFIED,
            "type": "Car",
            "engine": "Fuel",
            "licensePlate": PLATE,
        },
        "bookingType": "Day",
        "turn": TURN,
        "date": date,
        "seatId": [],
        "isGroupReservation": False,
        "isCarSharing": False,
    }

    # Este endpoit requiere de 3 datos , tenantId, zoneId y reservationId, los dos primeros
    # siempre son los mismos dado que solo se solicita plaza en Priegola o Victoria, pero el tercero
    # cambia, por lo que se debe extraer del pase de reserva que devuelve la cadena con 3 strings
    # https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/ + tenantId + %7C + zoneId + %7C + reservationId

    # URL del endpoint - Priegola
    # url = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7Ca91ee11f-a0c5-4a91-a2c5-f6d0642f1dff%7C" + reservation_id

    # URL del endpoint - Victoria
    url = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7C" + zone_to_use + "%7C" + reservation_id
    # url = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7C35e0550e-953a-41b5-ba97-cacaa4a44160%7C" + reservation_id

    # Realizando la peticion
    spinner.text = "Reservando plaza."
    try:
        API.write_log("Reservando plaza...")
        API.write_log("Endpoint: " + url)
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        # reserved_zone = response.json()
        API.write_log(f'Estado de la respuesta de la peticion de plaza: {response.status_code}')
        API.write_log(f'Texto de la respuesta de la peticion de plaza: {response.text}')

        # Crear el directorio 'res' si no existe
        if not os.path.exists("res"):
            os.makedirs("res")

        # Peticion aprobada, logica de verificacion de reserva de plaza
        spinner.text = "Peticion aprobada, comprobando reserva."
        if response.status_code == 200:
            spinner.succeed("Peticion aprobada!")
            spinner.text = "Comprobando reserva."
            API.write_log("Peticion aprobada, comprobando reserva...")
            try:
                # verifica si la respuesta es realmente un JSON
                reserved_zone = response.json()
                API.write_log('Peticion exitosa.')
                spinner.succeed('Peticion exitosa. Plaza reservada!')
                log("👍")
                API.write_log('Plaza reservada!.')
                API.write_log("Extrayendo datos de reserva en formato Json")

                filename = "reserved_zone.json"
                folder = "res"
                file_path = os.path.join(folder, filename)

                # Leer los datos existentes si el archivo ya existe
                spinner.text = "Extrayendo datos de reserva en formato Json."
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as json_file:
                        try:
                            existing_data = json.load(json_file)
                            spinner.succeed(f'Datos extraidos del archivo {filename}')
                        except json.JSONDecodeError:
                            existing_data = []
                            spinner.fail("Error, datos json no extraídos")
                else:
                    existing_data = []

                # Añadir la nueva respuesta a los datos existentes
                existing_data.append(reserved_zone)

                # Escribir todos los datos (incluyendo la nueva respuesta) en el archivo JSON
                with open(file_path, "w", encoding="utf-8") as json_file:
                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                API.write_log(f"Dato de la plaza reservada guardados dentro de la carpeta {folder}, revisa el archivo {filename}")
                spinner.succeed("Datos de plaza reservada extraidos!")
                return reserved_zone

            except json.JSONDecodeError:
                # Manejo del caso en que la respuesta es solo una cadena de texto
                API.write_log('La respuesta no es un JSON válido.')
                API.write_log('Peticion denegada.')
                spinner.fail('La respuesta no es un JSON válido. Petición Denegada!')
                log("👎")
                API.write_log('Plaza no reservada. Revisa el calendario')
                API.write_log(f'Respuesta recibida: {response.text}')
                spinner.fail('Plaza no reservada. Revisa el calendario')

                failed_response = response.text
                filename = "failed_response.txt"
                folder = "res"

                # Guardar la fecha en un archivo JSON dentro de la carpeta 'res'
                spinner.text = "Guardando fecha de archivo JSON"
                with open(os.path.join(folder, filename), "w") as text_file:
                    text_file.write(failed_response)
                    API.write_log(f"Respuesta fallida guardada dentro de la carpeta {folder}, revisa el archivo {filename}")
                    spinner.fail(f"Respuesta fallida guardada dentro de la carpeta {folder}, revisa el archivo {filename}")
                return -1
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            API.write_log(f"Error HTTP: 401, El servidor rechaza la peticion. El token usado no es valido, Detalles: {response.text}")
            return -2
        elif response.status_code == 502:  # Aquí verificamos si es un error 502 Bad Gateway
            API.write_log(f"Error HTTP: 502 Server Error: Bad Gateway, Detalles: {response.text}")
            spinner.fail(f"Error HTTP: 502 Server Error: Bad Gateway, Detalles: {response.text}")
            return -3  # Retornamos -3 como indicaste
        else:
            API.write_log(f"Error HTTP: {http_err}, Detalles: {response.text}")
            spinner.fail(f"Error HTTP: {http_err}, Detalles: {response.text}")
            return None

    except Exception as e:
        API.write_log(f"Error HTTP: {e}, Detalles: {response.text}")
        spinner.fail(f"Error HTTP: {e}, Detalles: {response.text}")
        return None


# https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7C35e0550e-953a-41b5-ba97-cacaa4a44160%7Ca1c39312-9092-4b6f-a295-37354f7262a7

# token2 = "eyJhbGciOiJSUzI1NiIsImtpZCI6InpWVjNyd2hYSlRZRVRnWlczeG9BSnBia0Vienl0T01TWjctS3U2SHZISzAiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiIzOWU5ZTkyZS04ZjQ2LTQwNGQtODAxNC1lYjg0YjJkZjBkODkiLCJuYW1lIjoiRGF2aWQiLCJPTVRlbmFudElkIjoiN2E5MDNhYzYtYWViNS00Y2Y4LTg3OWMtYzQ4ZjAyZmMzNmU3IiwiT01TdWJzY3JpcHRpb25FbmFibGVkIjp0cnVlLCJPTVN1YnNjcmlwdGlvbkV4cGlyYXRpb25EYXRlIjoxNzQ2MDg2NDAwLCJPTVVzZXJFbmFibGVkIjp0cnVlLCJPTUdyb3VwcyI6ImZmNTBjNzU3LTczYTktNDZiZC05OTFlLTVkYmVlMTIwNDAwYjthODNhYWM4ZC0xNGU5LTQwNzAtYmU3Zi02YmE0NWE4ZjQzN2EiLCJPTVJvbGVzIjoiUGFya2luZ0FwcFVzZXI7Um9vbUFwcFVzZXIiLCJ0aWQiOiI0NTg0OTJlYi1mMjhiLTQxNGQtOThkZC0xYmYzMWE3YjQ1M2YiLCJwYXNzd29yZEV4cGlyZWQiOmZhbHNlLCJub25jZSI6ImQyNDY3MzUwLWYzNWUtNDVmZS1iMDQwLTI2NTNkYWEzN2Y3OSIsInNjcCI6ImFjY2Vzc19hc191c2VyIiwiYXpwIjoiNTM0MTZhOTItODVhYS00Yzg2LWJkZTAtM2MwNmE3ZmQ4YzAwIiwidmVyIjoiMS4wIiwiaWF0IjoxNzA5MjA5NDcxLCJhdWQiOiI2ZDc3NDkzYS0yNGYwLTQ1YmMtYjYxZC0zNDE5YjU5MTAzNWQiLCJleHAiOjE3MDkyMTMwNzEsImlzcyI6Imh0dHBzOi8vbWFuYWdlcm9mZmljZS5iMmNsb2dpbi5jb20vNDU4NDkyZWItZjI4Yi00MTRkLTk4ZGQtMWJmMzFhN2I0NTNmL3YyLjAvIiwibmJmIjoxNzA5MjA5NDcxfQ.Dj4sFAFTeYlHEAzLF4_LrB2fKTXOUIdYgvwnoC-D9IBD9kNzAqVLVzrJKGYfc-wd1TB80OrOY8-EFHLsggJua4henaoRIvCCUtbQjBZUrrnRD6un83PM9UpchMQarhEZd-8YS9nplm5qqVTpWbA6j2WwDnUX1ax1NgzJDwH_DZmNuzjyHlQ6ndMbI5uURPDHnp-KLWUChrZLXgycPadSE6b8gfPZDA3RuSgAOcqsR6NJ7aiqLAxGpeNcboBLBYls-sacGVi-4MMjBbdcq17OKxc9r3AAaFKTtPGmrbG26ABy0-PjTQ0HbU6epA_OGWFBS-6pCTXkykuYLIJkKfcNFg"

# reservationID_test = "af61e59e-e8cd-47d0-a8a8-eba071ae6fd2"

# jpondatatest = load_data_place(reservationID_test, token2)
# result = extract_information(jpondatatest)
# print(jpondatatest)
# # print(result)
