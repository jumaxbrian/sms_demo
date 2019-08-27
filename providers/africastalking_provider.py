import os
import africastalking

class AfricasTalking:

    def __init__(self):
        AT_API_KEY = os.getenv("AT_API_KEY")
        AT_USERNAME = os.getenv("AT_USERNAME")
        africastalking.initialize(AT_USERNAME, AT_API_KEY)
        self.sms = africastalking.SMS

    def sanitize_phone_no(self, phone_no):
        pass
        # if phone_no is not None and phone_no[0] 

    def send(self, sender=None, recipient=None, msg=None):
        try:
            temp_response = self.sms.send(msg, [recipient])
            response = {
                "status": "success",
                "messageId": temp_response["SMSMessageData"]["Recipients"][0]["messageId"],
                "cost": temp_response["SMSMessageData"]["Recipients"][0]["cost"],
                "number": temp_response["SMSMessageData"]["Recipients"][0]["number"],
                "description": None
            }

        except Exception as e:
            response = {
                "status": "error",
                "description": str(e)
            }

        return response
        
