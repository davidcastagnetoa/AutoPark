from datetime import datetime

text = "2023-12-25"

try:
    # Intenta convertir el texto recibido en una fecha
    date_to_query = datetime.strptime(text, "%Y-%m-%d")
    # Procesa la fecha si es válida...
    print(f"Fecha válida recibida: {text}")
    # Aquí continuarías con la lógica para eliminar la reserva...
except ValueError:
    # Si falla la conversión, envía un mensaje de error
    print("Formato de fecha incorrecto. Por favor, usa el formato YYYY-MM-DD.")
