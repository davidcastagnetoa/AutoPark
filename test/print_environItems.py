# Imprimir todas las variables de entorno de la maquina actual
import os

for key, value in os.environ.items():
    print(f"{key}: {value}")
