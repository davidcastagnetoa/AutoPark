#!/bin/bash

cat << "EOF" | lolcat

                                     .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!.
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$ 
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P 
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$# 
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$* 
      ^$$$B  $$$$\     $$$$$$$$$$$$   d$$R" 
        "*$bd$$$$      '*$$$$$$$$$$$o+#" 
             """"          """"""" 
             
    ╔────────────────────────────────────╗
    |  Soy el principio de la eternidad, |
    |  el tercero en cada cuento,        |
    |  estoy donde comienza el espacio   |
    |  y existo en mitad del tiempo!     |
    ┖────────────────────────────────────┙

EOF

# Cambiar al directorio del script y .env
cd /home/admin/documents/AutoPark

# Activar un entorno virtual
source venv/bin/activate

# Ejecutar script en el entorno
python3 main.py

# Desactivar entorno virtual
deactivate
