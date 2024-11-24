from flask import Blueprint, jsonify, request
import requests
import os

BASE_URL = "https://api.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

p2p_transfer_blueprint = Blueprint('p2p_transfer', __name__)

@p2p_transfer_blueprint.route('/p2p-transfer', methods=['POST'])
def p2p_transfer():
    data = request.json
    payload = {
        "debitCurrency": data.get('debitCurrency', 'USD'),
        "interledgerWallets": data.get('interledgerWallets', [])
    }

    try:
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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
