from flask import Blueprint, jsonify, request
import requests
import os

BASE_URL = "https://api.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

create_user_blueprint = Blueprint('create_user', __name__)

@create_user_blueprint.route('/create-user', methods=['POST'])
def create_user():
    data = request.json
    payload = {
        "name": data.get('name'),
        "email": data.get('email'),
        "phoneNumber": data.get('phoneNumber')
    }

    try:
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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
