## Project Overview
This repository demonstrates how to use Flask to interact with Chimoney's API for financial operations. The application features endpoints for creating users, issuing Interledger payment pointers, executing P2P transfers, and verifying payments. This guide will help you set up the application, understand its structure, and test it using Postman.

For more details about Chimoney's API, visit the [Chimoney API Documentation](https://chimoney.readme.io/reference/introduction). If you have any questions or need assistance, please contact the Chimoney team at team@chimoney.io.

## Features
- Create User: Register users with Chimoney's API.
- Issue Payment Pointer: Generate an Interledger Payment Pointer for users.
- P2P Transfer: Facilitate peer-to-peer transfers using Interledger Wallets.
- Verify Payment: Check the status of payment transactions.


## Setup Instructions
Step 1: Clone the Repository

```
git clone https://github.com/your-repository/flask-chimoney-api.git

cd flask-chimoney-api
```

Step 2: Set Up a Virtual Environment
```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

Step 3: Install Dependencies
```
Step 3: Install Dependencies
```

Step 4: Configure Environment Variables
Create a .env file in the project directory with the following content:
```
CHIMONEY_API_KEY=your_chimoney_api_key
```
Replace your_chimoney_api_key with your actual Chimoney API key.

Step 5: Review app.py
The app.py file initializes the Flask app, loads environment variables, and registers Blueprints for all endpoints.

code snippet of app.py:
```
from flask import Flask, jsonify
from endpoints.create_user import create_user_blueprint
from endpoints.issue_pointer import issue_pointer_blueprint
from endpoints.p2p_transfer import p2p_transfer_blueprint
from endpoints.verify_payment import verify_payment_blueprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(create_user_blueprint)
app.register_blueprint(issue_pointer_blueprint)
app.register_blueprint(p2p_transfer_blueprint)
app.register_blueprint(verify_payment_blueprint)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Chimoney Flask API!"})

if __name__ == '__main__':
    app.run(debug=True)
```

## Endpoints
All endpoints are modularized into separate files under the endpoints folder. Below is the explanation and code snippet for each endpoint:

__init__.py in the endpoints folder
The __init__.py file ensures that the endpoints folder is recognized as a Python package. It may be left empty or used to initialize package-level settings.

code snippet of __init__.py
```
# __init__.py for endpoints package
```

1. Create User
Registers a new user with Chimoney's API.
- Request
    - URL: http://127.0.0.1:5000/create-user
    - Method: POST
    - Payload
```
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phoneNumber": "+1234567890"
}
```

code snippet of create_user.py
```
from flask import Blueprint, request, jsonify
import requests
import os

create_user_blueprint = Blueprint('create_user', __name__)
BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

@create_user_blueprint.route('/create-user', methods=['POST'])
def create_user():
    data = request.json
    payload = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phoneNumber": data.get("phoneNumber")
    }
    response = requests.post(
        f"{BASE_URL}/multicurrency-wallets/create",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": CHIMONEY_API_KEY
        },
        json=payload
    )
    return jsonify(response.json()), response.status_code
```

2. Issue Payment Pointer
Generates an Interledger Payment Pointer for a user.

- Request
    - URL: http://127.0.0.1:5000/issue-payment-pointer
    - Method: POST
    - Payload:
```
{
  {
  "userID": "", #userid generated from the usercreation
  "ilpUsername": "tundebaba" #input any name to be used for the creation of the ILP payment pointer 
}
```
code snippet of issue_pointer.py
```
from flask import Blueprint, request, jsonify
import requests
import os

issue_pointer_blueprint = Blueprint('issue_pointer', __name__)
BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

@issue_pointer_blueprint.route('/issue-payment-pointer', methods=['POST'])
def issue_payment_pointer():
    data = request.json
    payload = {
        "userID": data.get("userID"),
        "ilpUsername": data.get("ilpUsername", "default.user")
    }
    response = requests.post(
        f"{BASE_URL}/accounts/issue-wallet-address",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": CHIMONEY_API_KEY
        },
        json=payload
    )
    return jsonify(response.json()), response.status_code
```

3. P2P Transfer

Facilitates peer-to-peer transfers.

- Request
    - URL: http://127.0.0.1:5000/p2p-transfer
    - Method: POST
    - payload:
```
{
  "debitCurrency": "USD",
  "interledgerWallets": [
    {
      "amount": 50, ## set amount to be sent
      "walletAddress": "$ilp.example.receiver" ### the ilp payment pointer generated
    }
  ]
}
```

code snippet of p2p_transfer.py

```
from flask import Blueprint, request, jsonify
import requests
import os

p2p_transfer_blueprint = Blueprint('p2p_transfer', __name__)
BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

@p2p_transfer_blueprint.route('/p2p-transfer', methods=['POST'])
def p2p_transfer():
    data = request.json
    payload = {
        "debitCurrency": data.get("debitCurrency", "USD"),
        "interledgerWallets": data.get("interledgerWallets", [])
    }
    response = requests.post(
        f"{BASE_URL}/payouts/interledger-wallet-address",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": CHIMONEY_API_KEY
        },
        json=payload
    )
    return jsonify(response.json()), response.status_code
```

4. Verify Payment

Checks the status of a payment transaction.

- Request
    - URL: http://127.0.0.1:5000/verify-payment
    - Method: POST
    - Payload:

```
{
  "id": "abcdef123456" ## issueID of the transaction
}
```

code snippet of verify_payment.py

```
from flask import Blueprint, request, jsonify
import requests
import os

verify_payment_blueprint = Blueprint('verify_payment', __name__)
BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

@verify_payment_blueprint.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    payload = {"id": data.get("id")}
    response = requests.post(
        f"{BASE_URL}/payment/verify",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": CHIMONEY_API_KEY
        },
        json=payload
    )
    return jsonify(response.json()), response.status_code
```


## Run the Application
Start the Flask server:
```
python app.py
```

## Testing with Postman

- Create a new request for each endpoint.
- Set the method (e.g., POST) and URL (e.g., http://127.0.0.1:5000/create-user).
- Add required headers under the Headers tab:
    - Content-Type: application/json

- Enter the JSON payload in the Body tab, using raw mode.
- Send the request and check the response.


## Troubleshooting
- Ensure .env is set up with a valid Chimoney API key.
- Double-check request payload formatting.

## Resources for My talk
- [Chimoney API Documentation](https://chimoney.readme.io/reference/introduction)
- Mojaloop:
[Learn about Mojaloop's open-source platform for interoperable financial services.](https://mojaloop.io/)

- Interledger Protocol (ILP):
[Start building with Interledger and learn how it connects payment networks seamlessly.](https://interledger.org/developers/get-started/)
- Mifos:
[Discover Mifos' work in promoting financial inclusion through open-source banking.
Visit Mifos](https://mifos.org/)
- [Learn about Open Payment Standards](https://interledger.org/developers/blog/simple-open-payments-guide/)
- [Google Slides for the talk](https://docs.google.com/presentation/d/1Jc8KqQGj10By4h4qlPiRN6zMOfd48H0QKtLPFhQvP-8/edit?usp=sharing)
