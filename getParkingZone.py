import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Función auxiliar para log con fecha
def cl(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


# Cargando credenciales de acceso
load_dotenv()
URL = os.getenv("URL")


# Accede a la variable en formato JSON
json_data = os.getenv("JSON_DATA")
if json_data:
    config = json.loads(json_data)
    ZONE = config["zone"]
    PLATE = config["plate"]
    USERID = config["userId"]
    OFFICEID = config["officeId"]
    VEHICLEID = config["vehicleId"]
    DATETIMEVEHICLE_CREATED = config["createdAtUtc"]
    DATETIMEVEHICLE_MODIFIED = config["modifiedAtUtc"]
    TURN = config["turn"]
    # Acceder a otros valores en 'config' según sea necesario
else:
    cl("No se encontró la configuración JSON.")


# La fecha es 7 días después de hoy
date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
cl(f"Fecha a solicitar plaza: {date}")


# Reservar la plaza y Obtener su ID
def get_parking_place(secret):
    # URL del endpoint
    url = URL + "/BookingsByContext"

    # Construyendo los datos para la petición
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {secret}"}

    # Datos a enviar en el payload
    payload = {
        "userId": USERID,
        "officeId": OFFICEID,
        "zoneId": ZONE,
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

    if secret:
        # Realizar la petición POST
        try:
            cl("Reservando plaza...")
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Verificar el estado de la respuesta
            response.raise_for_status()
            cl("Plaza Reservada!!!")

            # La respuesta es una cadena de texto con los valores separados por |
            response_text = (
                response.text.strip()
            )  # Elimina espacios en blanco al inicio y al final
            values = response_text.split("|")

            # Asignar los valores a las variables correspondientes
            if len(values) >= 3:
                requestId = values[0].strip('"')
                zoneId = values[1].strip('"')
                reservationId = values[2].strip('"')

                # Imprimir o usar las variables según sea necesario
                cl("Extrayendo variables id de la plaza reservada...")
                cl(f"Request ID: {requestId}")
                cl(f"Zone ID: {zoneId}")
                cl(f"Reservation ID: {reservationId}")

                return requestId, zoneId, reservationId

            else:
                cl(
                    "Error al reservar la plaza, La respuesta no contiene los 3 valores."
                )

        except requests.exceptions.HTTPError as http_err:
            cl(f"Error HTTP: {http_err}, Detalles: {response.text}")
        except requests.exceptions.ConnectionError as conn_err:
            cl(f"Error de conexión: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            cl(f"Error de timeout: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            cl(f"Error general en la petición: {req_err}")

    else:
        cl("Se requiere el token para realizar la solicitud")
        return None, None, None


# Obtener los datos de la plaza reservada
def load_data_place(reservation_id, secret):
    # Construyendo los datos para la petición
    headers = {
        "Authorization": "Bearer " + secret,
        "Content-Type": "application/json; charset=utf-8",
    }
    # Datos a enviar en el payload
    body = {
        "userId": USERID,
        "officeId": OFFICEID,
        "zoneId": ZONE,
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

    # URL del endpoint
    url_info = (
        URL
        + "/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7C"
        + ZONE
        + "%7C"
        + reservation_id
    )

    if secret:
        # Realizando la petición
        try:
            cl("Obteniendo los datos de la plaza reservada...")
            print(url_info)
            response_data = requests.post(url_info, headers=headers, json=body)
            response_data.raise_for_status()
            data_result = response_data.json()
            cl("Petición exitosa.")
            cl(f"Estado de la respuesta: {response_data.status_code}")
            cl("Datos Extraidos en formato Json")
            print(f"Los datos obtenidos de la plaza son: {data_result}")

            # Crear el directorio 'res' si no existe
            if not os.path.exists("res"):
                os.makedirs("res")

            filename = "data_place.json"
            folder = "res"

            # Guardar los datos de la plaza reservada en un archivo JSON dentro de la carpeta 'res'
            with open(os.path.join(folder, filename), "w") as json_file:
                json.dump(data_result, json_file, ensure_ascii=False, indent=4)
                print(
                    f"Datos de plaza reservada dentro de la carpeta {folder} , revisa el archivo {filename}"
                )

        except requests.HTTPError as e:
            cl(f"Error HTTP: {e}")
        except Exception as e:
            cl(f"Error: {e}")

    else:
        cl("Se requiere el token para realizar la solicitud")


# Eliminar la plaza reservada
def delete_parking_place(secret, reservation_id):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {secret}",
    }

    body = {
        "userId": USERID,
        "reservationId": reservation_id,
    }

    DELETE_URL = (
        "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/"
        + body["reservationId"]
    )

    if secret:
        try:
            response = requests.delete(DELETE_URL, headers=headers, json=body)
            response.raise_for_status()

            if response.text:  # Verifica si hay contenido en la respuesta
                data = response.json()
                cl("Petición exitosa.")
                cl(f"Estado de la respuesta: {response.status_code}")
                cl(data)
                cl("Plaza eliminada correctamente")
            else:
                cl("Petición exitosa, pero no hay contenido en la respuesta.")

        except requests.HTTPError as e:
            cl(f"Error HTTP: {e}")
            cl("Error al eliminar la plaza")
        except Exception as e:
            cl(f"Error: {e}")
            cl("Error al eliminar la plaza")
