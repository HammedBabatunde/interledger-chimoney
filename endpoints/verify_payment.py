from flask import Blueprint, jsonify, request
import requests
import os

BASE_URL = "https://api.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

verify_payment_blueprint = Blueprint('verify_payment', __name__)

@verify_payment_blueprint.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    payload = {
        "id": data.get('id')
    }

    try:
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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
