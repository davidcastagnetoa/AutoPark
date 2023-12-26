import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Funcion auxiliar para log con fecha


def cl(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


# Cargando credenciales de acceso
load_dotenv()
URL = os.getenv("URL")


# Accede a la variable en formato JSON
json_data = os.getenv("JSON_DATA")
if json_data:
    config = json.loads(json_data)
    ZONE = config["zone_priegola_2"]
    PLATE = config["plate"]
    USERID = config["userId"]
    OFFICEID = config["officeId"]
    VEHICLEID = config["vehicleId"]
    DATETIMEVEHICLE_CREATED = config["createdAtUtc"]
    DATETIMEVEHICLE_MODIFIED = config["modifiedAtUtc"]
    TURN = config["turn"]
    # Acceder a otros valores en 'config' según sea necesario
else:
    cl("No se encontro la configuracion JSON.")


# La fecha es 5 días después de hoy
# date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

# La fecha actual
date = datetime.now().strftime("%Y-%m-%d")
cl(f"Fecha a solicitar plaza: {date}")


# Reservar la plaza y Obtener su ID
def get_parking_place(secret):
    # URL del endpoint
    url = URL + "/BookingsByContext"

    # Construyendo los datos para la peticion
    headers = {
        "Authorization": "Bearer " + secret,
        "Content-Type": "application/json; charset=utf-8",
    }

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

    reservationId = None

    if secret:
        # Realizar la peticion POST
        try:
            cl("Reservando plaza...")
            response = requests.post(
                url, headers=headers, data=json.dumps(payload))

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
                reservationId = values[2].strip('"')

                # Imprimir o usar las variables según sea necesario
                cl("Extrayendo variables id de la plaza reservada...")
                cl(f"Reservation ID: {reservationId}")
                return reservationId

            else:
                cl(
                    "Error al reservar la plaza, La respuesta no contiene los 3 valores."
                )
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400 and '409-11' in response.text:
                cl(f"No es posible reservar entre las 0:00 y 8:00 horas, Detalles: {response.text}")
                return -1
            elif response.status_code == 400 and 'It is not possible to select the weekend.' in response.text:
                cl(f"Error HTTP: 400 - No es posible seleccionar el fin de semana, Detalles: {response.text}")
                return -2
            elif response.status_code == 409 and '409-12' in response.text:
                cl(f"Error HTTP: 409 - Ya existe una plaza reservada a esta fecha, Detalles: {response.text}")
                return -3
            else:
                cl(f"Error HTTP: {http_err}, Detalles: {response.text}")
                return None
        except requests.exceptions.ConnectionError as conn_err:
            cl(f"Error de conexion: {conn_err}, Detalles: {response.text}")
        except requests.exceptions.Timeout as timeout_err:
            cl(f"Error de timeout: {timeout_err}, Detalles: {response.text}")
        except requests.exceptions.RequestException as req_err:
            cl(f"Error general en la peticion: {req_err}, Detalles: {response.text}")

    else:
        cl("Se requiere el token para realizar la solicitud")
        return None


def load_data_place(reservation_id, secret):
    # Construyendo los datos para la peticion
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
    url = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/Status/7a903ac6-aeb5-4cf8-879c-c48f02fc36e7%7Ca91ee11f-a0c5-4a91-a2c5-f6d0642f1dff%7C" + reservation_id

    # Realizando la peticion
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        reserved_zone = response.json()
        print(f'Estado de la respuesta: {response.status_code}')
        print('Peticion exitosa.')
        # print(reserved_zone)
        # Crear el directorio 'res' si no existe
        if not os.path.exists("res"):
            os.makedirs("res")

        print("Datos Extraidos en formato Json")

        filename = "reserved_zone.json"
        folder = "res"
        # Guardar la fecha en un archivo JSON dentro de la carpeta 'res'
        with open(os.path.join(folder, filename), "w") as json_file:
            json.dump(reserved_zone, json_file, ensure_ascii=False, indent=4)
            print(
                f"Datos guardados dentro de la carpeta {folder} , revisa el archivo {filename}"
            )

        return reserved_zone
    except requests.HTTPError as e:
        cl(f"Error HTTP: {e}, Detalles: {response.text}")
        return None
    except Exception as e:
        cl(f"Error HTTP: {e}, Detalles: {response.text}")
        return None


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
                cl("Peticion exitosa.")
                cl(f"Estado de la respuesta: {response.status_code}")
                cl(data)
                cl("Plaza eliminada correctamente")
            else:
                cl("Peticion exitosa, pero no hay contenido en la respuesta.")

        except requests.HTTPError as e:
            cl(f"Error HTTP: {e}")
            cl("Error al eliminar la plaza")
        except Exception as e:
            cl(f"Error: {e}")
            cl("Error al eliminar la plaza")
