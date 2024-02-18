# AutoPark: Automated Weekday Parking Space Reservation System Using Python and Selenium

Python program to automate booking parking spaces in a web application for a parking garage on weekdays. This Python script uses Selenium to open the browser in headless mode, log into the web application, and retrieve the necessary tokens from the `localstore`. Once the token is obtained, it will be used to send requests to the server and reserve a parking space in the private garage. Once reserved, it will send the details of the booked space via Telegram.

## Requirements

- Python 3.x
- Selenium WebDriver
- A WebDriver-compatible browser (Firefox, Chrome.)

## Installation

1. Install Python from [python.org](https://www.python.org/).
2. Create a virtual enviroment

   ```bash
   python -m venv venv
   ```

3. Activate the virtual enviroment

   On Windows System:

   ```bash
   source venv/Scripts/activate
   ```

   On Linux System:

   ```bash
   source venv/bin/activate
   ```

4. Install libraries using pip:

   ```bash
   pip install -r requirements.txt
   ```

   or if you are using Python 3, you may have to use pip3

   ```bash
   pip3 install -r requirements.txt
   ```

5. **Download WebDriver**  
   You will also need a WebDriver for interfacing with different web browsers.

   - **Geckodriver for Firefox**:  
     Download the appropriate version of Geckodriver for your system from [Geckodriver's GitHub releases](https://github.com/mozilla/geckodriver/releases).

   - **Chromedriver for Chrome**:  
     Download the correct version of Chromedriver based on your Chrome browser's version from [Chromedriver's download page](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Important Note

- Make sure to download the WebDriver version that corresponds to the version of the browser you are using. Otherwise, you might encounter compatibility issues.

## Configuration

1. Make sure to set up the `.env` file with the necessary environment variables:

   ```env
   USERNAME_HIBO="your_username"
   PASSWORD_HIBO="your_password"
   TELEGRAM_TOKEN="your_telegram_bot_token"
   CHAT_ID="your_telegram_chat_id"
   LINK="web_link"
   URL="api_link"
   ```

2. Import the environment variables into your script:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Setting Up Telegram

1. Create one by talking to @BotFather on Telegram.
2. Obtain the bot's token, which BotFather will provide upon the creation of the bot.
3. Start a conversation on your created bot's link
   ```env
   https://t.me/<Your Bot's Name>
   ```
4. To obtain your chat_id if you don't know it, search in your APP for a user named @userinfobot and type `/start`, then send a message to this bot. The ID will be displayed.

In these links, you will find manuals and examples for configuring the Telegram API:

- [orangepiweb.es](https://orangepiweb.es/telegram.php)
- [cosicasdeinformatica.com](http://cosicasdeinformatica.blogspot.com/2015/10/enviar-mensajes-de-telegram-desde-una.html)

## Usage

1. Run the script:

   ```bash
   python main.py
   ```

2. The script will open the browser, perform the login, and fetch the requested data from the `localStorage`.

## Despliegue de Aplicación Flask con Gunicorn y systemd

La aplicación Flask está diseñada para escuchar en un puerto específico (en este caso, el puerto 5000) y ejecutar una función en respuesta a mensajes recibidos a través de un bot de Telegram. Esta interacción permite una funcionalidad dinámica, donde las acciones específicas pueden ser desencadenadas por comandos enviados al bot.

### Configuración del Entorno

1. ##### Creación de un Entorno Virtual

Para mantener las dependencias organizadas y asegurar que nuestra aplicación se ejecute en un entorno aislado, crearemos un entorno virtual dedicado para nuestra aplicación Flask y Gunicorn.

```bash
python3 -m venv flaskvenv
```

2. ##### Activación del Entorno Virtual

Activa el entorno virtual para comenzar a instalar las dependencias necesarias.

```bash
source flaskvenv/bin/activate
```

3. ##### Instalación de Flask y Gunicorn

Con el entorno virtual activado, instala Flask y Gunicorn. Estos serán los componentes clave para servir tu aplicación.

```bash
pip install flask gunicorn
```

## Code Explanation

- The script uses Selenium to open up the browser and navigate to the specified URL.
- It fills in form fields using identifiers from the HTML elements.
- It runs a JavaScript script to pull data from `localStorage`.
- Extracts and displays specific keys from the JSON object stored in `localStorage`.
- Use this data to obtain the token and make a request to the server
- After receiving the response, make another web request to send a message via Telegram.

### Configuración del Servicio systemd

1. ##### Crear un Archivo de Unidad de Servicio systemd

Crea un archivo flaskapp.service en el directorio /etc/systemd/system/ con el siguiente contenido:

```bash
[Unit]
Description=Gunicorn instance to serve my Flask app
After=network.target

[Service]
User=<tu_usuario>
Group=<tu_grupo>
WorkingDirectory=/ruta/a/tu/app
Environment="PATH=/ruta/a/flaskvenv/bin"
ExecStart=/ruta/a/flaskvenv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

2. ##### Habilitar y Arrancar el Servicio
   Habilita el servicio para que se inicie en el arranque y luego arráncalo.

```bash
sudo systemctl enable flaskapp.service
sudo systemctl start flaskapp.service
```

3. ##### Recargar systemd para Aceptar Cambios
   Si realizas cambios en el archivo de servicio, recarga systemd para asegurarte de que se apliquen.

```bash
sudo systemctl daemon-reload
```

4. ##### Iniciar el Servicio Gunicorn
   Para iniciar el servicio después de cualquier ajuste o reinicio:

```bash
sudo systemctl restart flaskapp.service
```

5. #### Verificar el Estado del Servicio
   Comprueba el estado del servicio para asegurarte de que se está ejecutando correctamente.

```bash
sudo systemctl status flaskapp.service
```

6. #### Revisar Logs en Caso de Errores
   Si encuentras problemas o el servicio no se inicia correctamente, revisa los logs del sistema.

```bash
journalctl -u flaskapp.service
```

7. #### Detener el Servicio Gunicorn
   Si necesitas detener el servicio, utiliza:

```bash
sudo systemctl stop flaskapp.service
```

8. #### Configuración del Firewall
   Para permitir el tráfico en el puerto 5000, configura ufw con el siguiente comando:

```bash
sudo ufw allow 5000
sudo ufw status
```

## Important Notes

- The script handles exceptions for each action, outputting messages to the console if anything fails.
- The `localStorage` data is printed as JSON objects for easier future use.
- **This script is designed to function when there are more than three items in the `localStorage`.**
- **Before running the script, ensure you know which keys are stored in `localStorage` and their position. The script will extract values based on their position.**
