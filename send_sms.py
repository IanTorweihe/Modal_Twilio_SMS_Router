import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
import modal

#enviroment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
admin_phone = os.environ['ADMIN_PHONE'] #admin cell phone number
twilio_phone = os.environ['TWILIO_PHONE'] #twilio phone number

#modal stub definition
stub = modal.Stub("twilio-sms-test")

#modal image definition for twilio
twilio_image = modal.Image.debian_slim().pip_install("twilio")

#transfer local secrets to modal
stub["local_secrets"] = modal.Secret({
    "TWILIO_ACCOUNT_SID": account_sid,
    "TWILIO_AUTH_TOKEN": auth_token,
    "ADMIN_PHONE": admin_phone,
    "TWILIO_PHONE": twilio_phone
})

# Stub function to send test SMS message
@stub.function(secret=stub["local_secrets"], image=twilio_image)
def send_test_sms():
    """
    Send a test SMS message via Twilio from modal cloud
    """
    # Load local secrets
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    admin_phone = os.environ["ADMIN_PHONE"]
    twilio_phone = os.environ["TWILIO_PHONE"]

    # Send SMS message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="text from modal via twilio",
        from_=twilio_phone,
        to=admin_phone
    )
    return message.sid

# Stub function that recieves webhook from Twilio 
# that a message was sent from admin. Then routes that 
# message to all users on the distribution list 

@stub.local_entrypoint
def main():
   print(send_test_sms())


