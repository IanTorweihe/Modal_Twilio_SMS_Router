# Twilio SMS Routing with Modal

This repository contains two Python scripts, `route_sms.py` and `send_sms.py`, that demonstrate how to utilize the Twilio API for SMS services in conjunction with the Modal platform. 

## Overview

The Python scripts in this repository create a Modal cloud instance of a Flask application that interacts with the Twilio API to send and route SMS messages.

- `route_sms.py` is a Flask application that receives incoming SMS messages, verifies the sender, and forwards the messages to a distribution group if the sender is recognized as an admin. This application runs on a Modal cloud instance, offering scalability and simplicity of deployment.

- `send_sms.py` is a script that sends a test SMS to an admin phone number. This script also runs on a Modal cloud instance, demonstrating the simplicity of remote code execution.

## Prerequisites

To use these scripts, you'll need:

- A Modal account. If you don't have one, you can create one at [modal.com](https://modal.com).
- The `modal-client` package installed.
- A Twilio account with a valid account SID and auth token.
- An admin phone number and a Twilio phone number.

## Usage

1. Clone the repository to your local machine.
2. Load your environment variables.
3. Run the `send_sms.py` script to send a test SMS.
4. Deploy the `route_sms.py` script as a Flask app on a Modal cloud instance to handle incoming SMS.

## Disclaimer

Please ensure that you understand the implications of sending and forwarding SMS messages, including any costs associated with using the Twilio API.

## Acknowledgments

- Twilio API
- Modal Platform
- Flask
