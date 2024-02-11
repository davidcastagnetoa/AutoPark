from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    update = request.get_json()
    print("Received webhook:", update)

    # Procesar el comando /hello
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text == '/hello':
            print("Mensaje recibido: /hello")
            # Aquí puedes añadir más lógica, como responder al mensaje

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(port=5000)
