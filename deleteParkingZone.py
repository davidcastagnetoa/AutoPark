import requests
import os
import json
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
    spinner.succeed("Variables de entorno encontradas")
else:
    API.write_log("No se encontro la configuracion JSON.")
    spinner.fail("No se encontro la configuracion JSON.")


# Eliminar la plaza reservada (No en produccion)
def delete_parking_place(secret, reservation_id):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {secret}",
    }

    body = {
        "userId": USERID,
        "reservationId": reservation_id,
    }

    DELETE_URL = "https://office-manager-api.azurewebsites.net/api/Parking/Bookings/" + reservation_id

    if secret:
        try:
            response = requests.delete(DELETE_URL, headers=headers, json=body)
            response.raise_for_status()

            if response.text:  # Verifica si hay contenido en la respuesta
                data = response.json()
                API.write_log("Peticion exitosa.")
                API.write_log(f"Estado de la respuesta: {response.status_code}")
                API.write_log(data)
                API.write_log("Plaza eliminada correctamente")
            else:
                API.write_log("Peticion exitosa, pero no hay contenido en la respuesta.")

        except requests.HTTPError as e:
            API.write_log(f"Error HTTP: {e}")
            API.write_log("Error al eliminar la plaza")
        except Exception as e:
            API.write_log(f"Error: {e}")
            API.write_log("Error al eliminar la plaza")
