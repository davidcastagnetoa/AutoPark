from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    update = request.get_json()
    print("Received webhook:", update)
    # Aquí puedes procesar el update de Telegram según necesites
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(port=5000)
