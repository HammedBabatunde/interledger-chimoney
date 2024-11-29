from flask import Blueprint, jsonify, request
import requests
import os

BASE_URL = "https://api-v2-sandbox.chimoney.io/v0.2"
CHIMONEY_API_KEY = os.getenv("CHIMONEY_API_KEY")

if not CHIMONEY_API_KEY:
    raise ValueError("CHIMONEY_API_KEY environment variable is not set")

get_user_details_blueprint = Blueprint('get_user_details', __name__)

@get_user_details_blueprint.route('/get-user-details', methods=['GET'])
def get_user_details():
    data = request.json

    if not data or 'id' not in data:
        return jsonify({"error": "userID is required"}), 400

    id = data.get('id')

    try:
        response = requests.get(
            f"{BASE_URL}/multicurrency-wallets/get",
            headers={
                "accept": "application/json",
                "X-API-KEY": CHIMONEY_API_KEY
            },
            params={"id": id}
        )

        if response.status_code == 200:
            try:
                return jsonify(response.json()), 200
            except ValueError:
                return jsonify({"error": "Invalid JSON response"}), 500
        else:
            return jsonify({"error": "Failed to get user details", "status_code": response.status_code, "response": response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500