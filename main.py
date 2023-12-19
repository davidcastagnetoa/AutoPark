from getTokensParking import getToken
from getParkingZone import get_parking_place, load_data_place

# from getAvailabilityZones import getAvailabilityZones
# from getParkingZone import delete_parking_place

if __name__ == "__main__":
    # print("CONSULTA DE TOKEN \n")
    secret_access = getToken()
    if secret_access is not None:
        ## Consulta plazas disponibles (aun en desarrollo)
        # getAvailabilityZones(secret_access)

        ## Reserva la plaza (la primera disponible)
        # print("\nACCEDIENDO A RESERVA DE PLAZA")
        requestId, zoneId, reservationId = get_parking_place(secret_access)

        ## Obtenie los datos de la plaza reservada
        # print("\nACCEDIENDO A CONSULTA DE PLAZA")
        load_data_place(reservationId, secret_access)

        ## Elimina la plaza reservada
        # delete_parking_place(secret_access, reservationId)
