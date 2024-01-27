import pickle
import json
import os

# Ruta al archivo .pkl
ruta_archivo_cookies = 'HyboCookies.pkl'
# Ruta al nuevo archivo .json
ruta_archivo_json = 'res/HyboCookies.json'

try:
    # Cargar las cookies desde el archivo .pkl
    with open(ruta_archivo_cookies, 'rb') as file:
        cookies = pickle.load(file)

    # Guardar las cookies en un archivo .json
    with open(ruta_archivo_json, 'w') as file:
        json.dump(cookies, file, indent=4)

    print(f"Las cookies han sido guardadas en {ruta_archivo_json}.")

except FileNotFoundError:
    print(f"Archivo no encontrado: {ruta_archivo_cookies}")
except Exception as e:
    print("Error al convertir las cookies:", e)
