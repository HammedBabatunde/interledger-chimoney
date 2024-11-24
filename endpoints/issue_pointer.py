from flask import Blueprint, jsonify, request
import requests
import os

BASE_URL = "https://api.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

issue_pointer_blueprint = Blueprint('issue_pointer', __name__)

@issue_pointer_blueprint.route('/issue-payment-pointer', methods=['POST'])
def issue_payment_pointer():
    data = request.json
    payload = {
        "userID": data.get('userID'),
        "ilpUsername": data.get('ilpUsername', 'default.user')
    }

    try:
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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
