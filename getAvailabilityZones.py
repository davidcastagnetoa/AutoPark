# import inquirer
import requests
import numpy as np
from datetime import datetime
import os
import json

# Obtener fecha de entrada


def validate_date(answer, current):
    try:
        datetime.strptime(current, "%Y-%m-%d")
        return True
    except ValueError:
        return "This is not a valid date. Please use the format YYYY-MM-DD."


# Obtener Fechas de salida
def sumar_dias_laborables(fecha_inicial, dias_a_sumar):
    endDate = np.busday_offset(fecha_inicial, dias_a_sumar, roll="forward")
    return str(endDate)


# Solicitar Plazas
def getAvailabilityZones(secret_access):
    # questions = [
    #     inquirer.Text(
    #         "date", message="Introduce una fecha (YYYY-MM-DD)", validate=validate_date
    #     )
    # ]

    # answers = inquirer.prompt(questions)
    # startDate = answers["date"]
    startDate = datetime.now().strftime("%Y-%m-%d")
    print("the startDate value is :", startDate)

    endDate = sumar_dias_laborables(startDate, 5)
    print("the endDate value is :", endDate)

    url = (
        "https://office-manager-api.azurewebsites.net/api/Parking/GetAvailabilityZones"
    )
    headers = {
        "Authorization": "Bearer " + secret_access,
        "Content-Type": "application/json",
    }
    # Parámetros de consulta
    params = {
        "officeId": "9b122c05-e7d6-4ce4-9936-0d3a8cfcc6c8",
        "startDate": startDate,
        "endDate": endDate,
    }
    try:
        response = requests.get(url, headers=headers,
                                params=params)  # Peticion GET
        # Comprobar si la respuesta tiene un codigo de estado exitoso
        response.raise_for_status()
        print(f"Estado de la respuesta: {response.status_code}")
        data = response.json()

        # Crear el directorio 'res' si no existe
        if not os.path.exists("res"):
            os.makedirs("res")

        print("Datos Extraidos en formato Json")

        filename = "available_zones.json"
        folder = "res"
        # Guardar la fecha en un archivo JSON dentro de la carpeta 'res'
        with open(os.path.join(folder, filename), "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(
                f"Datos guardados dentro de la carpeta {folder} , revisa el archivo {filename}"
            )

    except requests.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        return
    except requests.ConnectionError as conn_err:
        print(f"Error de conexion: {conn_err}")
        return
    except requests.Timeout as timeout_err:
        print(f"Error de timeout: {timeout_err}")
        return
    except requests.RequestException as req_err:
        print(f"Error general: {req_err}")
        return
    except TypeError:
        print("Tipo de dato incorrecto, se esperaba un diccionario")
        return


# Hacer solictudes de plaza en cada una de las plazas libres, en cuanto obtenga y response.status_code 200 obtener datos de plaza, fecha, edificio y horario
