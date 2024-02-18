import requests
import os
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.logger import log, API
from halo import Halo

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
    PLATE = config["plate"]
    USERID = config["userId"]
    OFFICEID = config["officeId"]
    VEHICLEID = config["vehicleId"]
    DATETIMEVEHICLE_CREATED = config["createdAtUtc"]
    DATETIMEVEHICLE_MODIFIED = config["modifiedAtUtc"]
    TURN = config["turn"]
    # Acceder a otros valores en 'config' según sea necesario
    spinner.succeed("Variables de entorno cargadas")
else:
    API.write_log("No se encontro la configuracion JSON.")
    spinner.fail("No se encontro la configuracion JSON.")


def reservedPlaceData(date):
    # Conectar a la base de datos
    conn = sqlite3.connect('reservas.db')
    try:
        cursor = conn.cursor()

        # Formatear la fecha para la consulta, si es necesario
        formatted_date = date.strftime("%d %B de %Y")

        # Realizar la consulta SQL para encontrar el ID de reserva por fecha
        cursor.execute("SELECT id, plaza, zona, turno, matricula, fecha FROM reservas WHERE fecha = ?", (formatted_date,))

        result = cursor.fetchone()  # Obtener el primer resultado

        if result:
            reserved_id = result[0]  # Obtener el ID de reserva del resultado
            reserved_plaza = result[1]
            reserved_zona = result[2]
            reserved_turno = result[3]
            reserved_matricula = result[4]
            reserved_fecha = result[5]
            spinner.succeed(f"Date: {date}")
            API.write_log(f"Date: {date}")
            spinner.succeed(f"The Reservation Id: {reserved_id}")
            API.write_log(f"The Reservation Id: {reserved_id}")
            return reserved_id, reserved_plaza, reserved_zona, reserved_turno, reserved_matricula, reserved_fecha
        else:
            spinner.fail(f"No reservations found for the date: {date}")
            API.write_log(f"No reservations found for the date: {date}")
            return None, None, None, None, None, None  # Retornar None si no se encuentra un resultado

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()


# Eliminar la plaza reservada (No en produccion)
def delete_parking_place(secret, reserved_id):
    spinner.succeed(f"Reservation Id de reserva a eliminar: {reserved_id}")
    API.write_log(f"Reservation Id de reserva a eliminar: {reserved_id}")

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {secret}",
    }

    body = {
        "userId": USERID,
        "reservationId": reserved_id,
    }

    DELETE_URL = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/" + reserved_id

    if secret:
        try:
            response = requests.delete(DELETE_URL, headers=headers, json=body)
            response.raise_for_status()

            if response.text:  # Verifica si hay contenido en la respuesta
                data = response.json()

                spinner.succeed("Peticion exitosa.")
                API.write_log("Peticion exitosa.")

                spinner.succeed(f"Estado de la respuesta: {response.status_code}")
                API.write_log(f"Estado de la respuesta: {response.status_code}")

                API.write_log(data)

                spinner.succeed("Plaza eliminada correctamente")
                API.write_log("Plaza eliminada correctamente")

                spinner.stop()
                return True
            else:
                spinner.fail("Peticion exitosa, pero no hay contenido en la respuesta.")
                API.write_log("Peticion exitosa, pero no hay contenido en la respuesta.")
                spinner.stop()
                return False

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                spinner.fail(f"Error HTTP: 401, El servidor rechaza la peticion. El token usado no es valido, Detalles: {response.text}")
                API.write_log(f"Error HTTP: 401, El servidor rechaza la peticion. El token usado no es valido, Detalles: {response.text}")
                spinner.stop()
                return -5
            elif response.status_code == 404 and 'Object reference not set to an instance of an object.' in response.text:  # Suponiendo que 404 es el código de error para objeto no encontrado
                spinner.fail("Error HTTP: 404, La plaza de garaje especificada no existe o ya fue eliminada")
                API.write_log(f"Error HTTP: 404, La plaza de garaje especificada no existe o ya fue eliminada, Detalles: {response.text}")
                spinner.stop()
                return -6
            else:
                API.write_log(f"Error HTTP: {http_err}, Detalles: {response.text}")
                spinner.fail(f"Error HTTP: {http_err}, Detalles: {response.text}")
                spinner.stop()
                return False
        except requests.exceptions.ConnectionError as conn_err:
            API.write_log(f"Error de conexion: {conn_err}, Detalles: {response.text}")
            spinner.fail(f"Error de conexion: {conn_err}, Detalles: {response.text}")
            spinner.stop()
            return False
        except requests.exceptions.Timeout as timeout_err:
            API.write_log(f"Error de timeout: {timeout_err}, Detalles: {response.text}")
            spinner.fail(f"Error de timeout: {timeout_err}, Detalles: {response.text}")
            spinner.stop()
            return False
        except requests.exceptions.RequestException as req_err:
            API.write_log(f"Error general en la peticion: {req_err}, Detalles: {response.text}")
            spinner.fail(f"Error general en la peticion: {req_err}, Detalles: {response.text}")
            spinner.stop()
            return False
        except Exception as e:
            API.write_log(f"Error: {e}")
            spinner.fail("Error al eliminar la plaza")
            API.write_log("Error al eliminar la plaza")
            spinner.stop()
            return False

    else:
        API.write_log("Se requiere el token para realizar la solicitud")
        spinner.fail("Se requiere el token para realizar la solicitud")
        spinner.stop()
        return False


# # EJEMPLO DE USO
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InpWVjNyd2hYSlRZRVRnWlczeG9BSnBia0Vienl0T01TWjctS3U2SHZISzAiLCJ0eXAiOiJKV1QifQ"
# # Crear un objeto datetime para el 25 de diciembre de 2023

# text = "2023-12-25"

# try:
#     # Intenta convertir el texto recibido en una fecha
#     date_to_query = datetime.strptime(text, "%Y-%m-%d")
#     # Procesa la fecha si es válida...
#     print(f"Fecha válida recibida: {text}")
#     # Aquí continuarías con la lógica para eliminar la reserva...
# except ValueError:
#     # Si falla la conversión, envía un mensaje de error
#     print("Formato de fecha incorrecto. Por favor, usa el formato YYYY-MM-DD.")

# # Obtener el ID de reserva para la fecha especificada
# reservedID, plaza, zona, turno, matricula, fecha = reservedPlaceData(date_to_query)
# message = "<b>Plaza: </b>" + plaza + "\n" + "<b>Zona: </b>" + zona + "\n" + "<b>Turno: </b>" + turno + "\n" + "<b>Matrícula: </b>" + matricula + "\n" "<b>Fecha: </b>" + fecha
# print(message)
# # Ejecutar la eliminacion de la plaza
# delete_parking_place(token, reservedID)
