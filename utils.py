from providers.nexmo_provider import Nexmo
from providers.africastalking_provider import AfricasTalking
import settings

FINAL_STATUS = ["rejected", "buffered", "delivered", "failed"]
NEXMO_ERRORS = {
    "1": "Unknown",
    "2": "Absent Subscriber",
    "3": "Absent Subscriber",
    "4": "Call Barred by User",
    "5": "Portability Error",
    "6": "Anti-Spam Rejection",
    "7": "Handset Busy",
    "8": "Network Error",
    "9": "Illegal Number",
    "10": "Illegal Message",
    "11": "Unroutable",
    "12": "Destination Unreachable",
    "13": "Subscriber Age Restriction",
    "14": "Number Blocked by Carrier",
    "15": "Prepaid Insufficient Funds",
    "99": "General Error"
}

def sanitize_africastalking_delivery(delivery):
    # ImmutableMultiDict([('phoneNumber', '+254712040487'), ('networkCode', '63902'), ('retryCount', '0'), ('id', 'ATXid_0f7465c8ced18e65c472ddc421980b95'), ('status', 'Success')])
    status = delivery["status"].lower()
    if status == "success":
        status = "delivered"
    response = None
    if status in FINAL_STATUS:
        #process response   
        response = {
            "phone_number": delivery["phoneNumber"],
            "network_code": delivery["networkCode"],
            "id": delivery["id"],
            "status": status,
            "failure_reason": delivery.get("failureReason")
        }

    return response

def sanitize_nexmo_delivery(delivery):
    # ImmutableMultiDict([('to', 'Acme Inc 2'), ('scts', '1908281615'), ('status', 'delivered'), ('err-code', '0'), ('price', '0.05240000'), ('message-timestamp', '2019-08-28 16:15:02'), ('msisdn', '254712040487'), ('network-code', '63902'), ('messageId', '1500000056EC762F')])
    status = delivery["status"].lower()
    error_code = delivery.get("err-code")
    error = None
    if error_code != "0":
        error = NEXMO_ERRORS.get(error_code)

    response = None
    if status in FINAL_STATUS:
        response = {
            "phone_number": delivery["msisdn"],
            "network_code": delivery["network-code"],
            "id": delivery["messageId"],
            "status": delivery["status"].lower(),
            "failure_reason": error
        }

    return response

def send_sms():
    provider_list = [Nexmo(), AfricasTalking()]
    for provider in provider_list:
        while settings.messages_queue:
            data = settings.messages_queue.pop_left()
            response = provider.send(
                sender = data["sender"],
                recipient = data["recipient"],
                msg = data["msg"]
            )

            settings.messages_dict[data["recipient"]] = data

            