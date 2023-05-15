import os
from flask import Flask, request
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
load_dotenv()
import modal

# Load environment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
admin_phone = os.environ['ADMIN_PHONE']
twilio_phone = os.environ['TWILIO_PHONE']
dist_group_1 = os.environ['DIST_GROUP_1']
dist_group_2 = os.environ['DIST_GROUP_2']


# Create a Modal stub with a unique name
stub = modal.Stub("twilio-sms-test")


# Define a Modal image for the Twilio Python package
twilio_image = modal.Image.debian_slim().pip_install("twilio" , "flask", 
                                                 "flask-cors", "python-dotenv")


# Transfer local secrets to Modal, including Twilio credentials 
# and phone numbers
stub["local_secrets"] = modal.Secret({
    "TWILIO_ACCOUNT_SID": account_sid,
    "TWILIO_AUTH_TOKEN": auth_token,
    "ADMIN_PHONE": admin_phone,
    "TWILIO_PHONE": twilio_phone,
    "DIST_GROUP_1": dist_group_1,
    "DIST_GROUP_2": dist_group_2
})


# Define a route for handling incoming SMS messages
def handle_incoming_sms(app, client):
    @app.route("/", methods=['POST'])
    def inner_handle_incoming_sms():
        # load environment variables
        admin_phone = os.environ['ADMIN_PHONE']
        twilio_phone = os.environ['TWILIO_PHONE']
        dist_group_1 = os.environ['DIST_GROUP_1']
        dist_group_2 = os.environ['DIST_GROUP_2']
        # convert distribution group string to list
        distribution_group = (dist_group_1 + " " + dist_group_2).split()

        # Get the sender's phone number
        # and the SMS message body from the incoming request
        sender = request.values.get('From')
        body = request.values.get('Body')
        
        # Check if the sender is the admin
        if sender == admin_phone:
            # If the sender is the admin, loop through the distribution group
            for contact in distribution_group:
                # Send the message to each contact in the distribution group
                client.messages.create(
                    body=body,
                    from_=twilio_phone,
                    to=contact
                )

            # Create a TwiML response to send confirmation message to the admin
            response = MessagingResponse()
            response.message("Message sent to distribution group.")
            # Return the TwiML response as a string
            return str(response)
        else:
            # If the sender is not the admin, return a 403 Forbidden status
            return 'MODAL FAIL!', 403

    return inner_handle_incoming_sms



# Wrap the Flask app in a Modal stub function
@stub.wsgi(image=twilio_image, secret=stub["local_secrets"])
def sms_app():
    #imports for modal
    import os
    from flask import Flask, request
    from flask_cors import CORS
    from twilio.rest import Client
    from twilio.twiml.messaging_response import MessagingResponse
    from dotenv import load_dotenv
    load_dotenv()
    
    app = Flask(__name__)
    CORS(app)
    client = Client(account_sid, auth_token)

    # Add the route to the Flask app
    app.add_url_rule("/sms", "handle_incoming_sms", 
                     handle_incoming_sms(app, client), methods=['POST'])
    
    return app


