from flask import Flask, jsonify
from endpoints.create_user import create_user_blueprint
from endpoints.issue_pointer import issue_pointer_blueprint
from endpoints.p2p_transfer import p2p_transfer_blueprint
from endpoints.verify_payment import verify_payment_blueprint
from dotenv import load_dotenv
import os

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
