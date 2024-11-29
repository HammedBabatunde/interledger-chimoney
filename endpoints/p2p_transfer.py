from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the blueprint
p2p_transfer_blueprint = Blueprint('p2p_transfer', __name__)

# Chimoney API details
BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")


@p2p_transfer_blueprint.route('/p2p-transfer', methods=['POST'])
def p2p_transfer():
    """
    P2P transfer endpoint using Chimoney API.
    """
    # Request payload structure
    data = request.json

    # Example: Expected request format
    # {
    #   "interledgerWallets": [
    #       {
    #           "interledgerWalletAddress": "https://ilp-sandbox.chimoney.com/test-1",
    #           "currency": "USD",
    #           "amountToDeliver": 5
    #       }
    #   ],
    #   "debitCurrency": "USD"
    # }

    interledger_wallets = data.get('interledgerWallets', [])
    debit_currency = data.get('debitCurrency', 'USD')

    # Construct the payload
    payload = {
        "interledgerWallets": interledger_wallets,
        "debitCurrency": debit_currency
    }

    try:
        # API call
        response = requests.post(
            f"{BASE_URL}/payouts/interledger-wallet-address",
            json=payload,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": CHIMONEY_API_KEY
            }
        )

        # Return the Chimoney API response
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500