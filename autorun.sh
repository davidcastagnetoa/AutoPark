#!/bin/bash

# Cambiar al directorio del script y .env
cd /home/admin/documents/AutoPark

# # Activar un entorno virtual
# source venv/bin/activate

# # Ejecutar script en el entorno
# python3 main.py

# Ejecutar tu script compilado
./build/exe.linux-x86_64-3.11/main

# Dar permisos a autorun.sh
# chmod +x ./autorun.sh