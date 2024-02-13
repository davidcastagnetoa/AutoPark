import json
from datetime import datetime


def extract_information(json_data):
    # Asegurate de que json_data sea una lista y contenga al menos un elemento
    if not json_data:
        print(f"The type of json_data is {type(json_data)}")
        return None

    if not isinstance(json_data, list):
        print(f"json_data no es una lista. {json_data}")
        return -1

    if not json_data[0]:
        print(f"json_data es una lista vacia. {json_data}")
        return -2

    # Extraer la informacion del primer elemento de la lista
    data = json_data[0]

    # Extraer las variables requeridas
    plaza = data.get('seat', {}).get('name', '')
    zona = data.get('zone', {}).get('name', '')
    turno = data.get('turn', '')
    matricula = data.get('vehicle', {}).get('licensePlate', '')

    # Formatear la fecha
    fecha_raw = data.get('date', '')
    try:
        fecha_datetime = datetime.fromisoformat(fecha_raw)
        fecha = fecha_datetime.strftime("%d %B de %Y")
    except ValueError:
        fecha = ''

    return plaza, zona, turno, matricula, fecha


# Datos de ejemplo
# json_data = [{'id': '41d90c5c-1562-47ae-908b-367db1c7b776', 'objectType': 'OM.ParkingReservation', 'createdAtUtc': '2023-12-19T20:07:46.773371Z', 'userId': '39e9e92e-8f46-404d-8014-eb84b2df0d89', 'userName': 'David', 'officeId': '9b122c05-e7d6-4ce4-9936-0d3a8cfcc6c8', 'date': '2023-12-25T00:00:00', 'zoneId': 'a91ee11f-a0c5-4a91-a2c5-f6d0642f1dff', 'seatId': ['a41ae95a-b3da-461d-b599-95d8342e17ae'], 'turn': 'AllDay', 'zone': {'id': 'a91ee11f-a0c5-4a91-a2c5-f6d0642f1dff', 'objectType': 'OM.ParkingZone', 'name': 'Priegola - PS2 ', 'officeId': '9b122c05-e7d6-4ce4-9936-0d3a8cfcc6c8', 'mapImageUrl': 'https://officemanagerstorage.blob.core.windows.net/securitas/images/parkingzone/428cdfe8-ff5f-4ccb-8ab6-48ca0e82492b.png', 'tags': [], 'vehicleType': 'Car', 'vehicleEngineType': 'Fuel', 'currencyCode': 'EUR'}, 'seat': {'id': 'a41ae95a-b3da-461d-b599-95d8342e17ae', 'objectType': 'OM.ParkingSeat', 'name': '112', 'zoneId': 'a91ee11f-a0c5-4a91-a2c5-f6d0642f1dff', 'zone': 'Priegola - PS2', 'enabled': True, 'tags': [], 'mapPoints': {'x': 656.5, 'y': 1339.3, 'width': 105.0, 'height': 52.0}}, 'vehicle': {'id': '05411e97-7078-45c7-9452-a856a053bc69', 'objectType': 'OM.Vehicle', 'type': 'Car', 'engine': 'Fuel', 'licensePlate': '6516KJT'}, 'status': 'Pending', 'userBasicInformations': [], 'bookingType': 'Day'}]

# json_data = None
# json_data = [""]

# Llamar a la funcion con los datos de ejemplo
# result = extract_information(json_data)

# if result is None:
#     msg = "json_data is None."
#     print(msg)
# elif result == -1:
#     msg = "json_data no es una lista."
#     print(msg)
# elif result == -2:
#     msg = "json_data es una lista vacia."
#     print(msg)
# else:
#     plaza, zona, turno, matricula, fecha = result
#     print(f"Plaza: {plaza}")
#     print(f"Zona: {zona}")
#     print(f"Turno: {turno}")
#     print(f"Matricula: {matricula}")
#     print(f"Fecha: {fecha}")
