# Imprimir todas las variables de entorno
import os
for key, value in os.environ.items():
    print(f"{key}: {value}")
