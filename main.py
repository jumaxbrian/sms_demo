from flask import Flask, request, current_app
from os.path import join, dirname
from dotenv import load_dotenv

from providers.nexmo_provider import Nexmo
from providers.africastalking_provider import AfricasTalking

dotenv_path = join(dirname(__file__), "./.env")
load_dotenv(dotenv_path)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/api/v1/messages/", methods=['POST'])
def send():
    # sender, recipient, msg
    sender = request.form["sender"]
    recipient = request.form["recipient"]
    msg = request.form["msg"]
    # print(request.form)

    nexmo_provider = Nexmo()
    response = nexmo_provider.send(
        sender = "Acme Inc 2",
        recipient = "+254712040487",
        msg = "I am grateful!"
    )

    return response

@app.route("/api/v1/callback/at", methods=['POST'])
def callback_at():
    current_app.logger.debug('africastalking')
    print(request.form)

@app.route("/api/v1/callback/nexmo", methods=['POST'])
def callback_at():
    current_app.logger.debug('nexmo')
    print(request.form)

if __name__ == "__main__":   
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)