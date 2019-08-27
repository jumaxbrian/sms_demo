import os
import nexmo

class Nexmo:

    def __init__(self):
        NEXMO_API_KEY = os.getenv("NEXMO_API_KEY")
        NEXMO_API_SECRET = os.getenv("NEXMO_API_SECRET")
        self.client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

    def send(self, sender=None, recipient=None, msg=None):
        responseData = self.client.send_message(
            {
                "from": sender,
                "to": recipient,
                "text": msg,
            }
        )

        if responseData["messages"][0]["status"] == '0':
            cost = float(responseData["messages"][0].get("message-price"))*100
            response = {
                "status": "success",
                "messageId": responseData["messages"][0].get("message-id"),
                "cost": cost,
                "number": responseData["messages"][0].get("to"),
                "description": responseData["messages"][0].get("error-text")
            }

        else:
            response = {
                "status": "error",
                "description": responseData["messages"][0].get("error-text")
            }

        return response
        

