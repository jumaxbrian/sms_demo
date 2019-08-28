from flask import Flask, request, current_app, jsonify
from os.path import join, dirname
from dotenv import load_dotenv
import collections
from multiprocessing import Process

import settings
import utils

dotenv_path = join(dirname(__file__), "./.env")
load_dotenv(dotenv_path)

app = Flask(__name__)

settings.init() #initialize all global vars

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/api/v1/messages/", methods=['POST'])
def send():
    # sender, recipient, msg
    input_error = None
    try:
        sender = request.form["sender"]
        recipient = request.form["recipient"]
        msg = request.form["msg"]
        callback_url = request.form["callback_url"]
    except Exception as e:
        input_error = "There was error with your input. Ensure sender, recipient, msg and callback_url are specified"
    # print(request.form)

    if input_error:
        response =  jsonify({"error":input_error})
        response.status_code = 400
        return response

    settings.messages_queue.append({
        "sender": sender,
        "recipient": recipient,
        "msg": msg,
        "callback_url": callback_url
    })

    messages_processor = Process(name='Process Messages: ', target=utils.send_sms)
    messages_processor.start()

    response =  jsonify({"status":"submitted"})
    response.status_code = 200
    return response

@app.route("/api/v1/callback/at", methods=['POST'])
def callback_at():    
    current_app.logger.debug('africastalking callback')
    # print(request.form)
    data = utils.sanitize_africastalking_delivery(request.form)

    if data:
        phone_number = data["phone_number"]
        original_data = settings.messages_dict[phone_number]
        response = jsonify(data)
        response.status_code = 200
        sender_response = requests.post(original_data["callback_url"], json=response)
        log_msg = "{}: {}".format(
            str(sender_response),
            str(response)
        )
        current_app.logger.debug(log_msg)

    # response to service provider
    if data is None:
        response = jsonify({"None":"None"})
        response.status_code = 200
    
    return response

@app.route("/api/v1/callback/nexmo", methods=['POST'])
def callback_nexmo():
    current_app.logger.debug('nexmo callback')
    # print(request.form)
    data = utils.sanitize_nexmo_delivery(request.form)
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route("/api/v1/callback/dummy", methods=['POST'])
def dummy_sender_callback():
    current_app.logger.debug(request.form)
    response = jsonify({"None":"None"})
    response.status_code = 200
    return response

if __name__ == "__main__":   
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)