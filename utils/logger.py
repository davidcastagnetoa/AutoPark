from datetime import datetime


def log(msg):
    print("[{}]: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))


class API:
    @staticmethod
    def write_log(message, type="info"):
        try:
            with open('logs/api-{}.log'.format(type), 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except UnicodeEncodeError:
            print("[{}]: Error al escribir en el archivo. Caracter no soportado.".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Error inesperado: {str(e)}")
