import json
from pprint import pprint

from flask import Flask, jsonify, request, redirect

from util import keys, teleport

# Load config
with open("config.json", mode="r") as f:
    config = json.load(f)


app = Flask(__name__)


@app.route("/decrypt", methods=["GET"])
def decrypt_endpoint():
    data = request.args.get("data")
    if not data:
        return jsonify({"error": "No data provided"}), 400

    decrypted_data = keys.decrypt(data)

    teleport_jwt = request.headers.get("Teleport-Jwt-Assertion")

    if teleport_jwt:
        payload = teleport.process_jwt(teleport_jwt, config)
        roles = payload.get("roles", [])
        
    if decrypted_data.get("roles"):
        if decrypted_data["roles"] == []:
            decrypted_data["roles"] = ["any"]
        if not teleport.check_access(require=decrypted_data["roles"], have=roles):
            return jsonify({"error": "Access denied"}), 403

    # Retrieve the URL from the decrypted data
    url = decrypted_data.get("url")

    if not url:
        return jsonify({"error": "No URL found in the decrypted data"}), 400

    # Redirect the client to the URL
    return redirect(url)


@app.route("/", methods=["GET"])
def root_endpoint():
    # Check for a teleport JWT header
    teleport_jwt = request.headers.get("Teleport-Jwt-Assertion")

    if teleport_jwt:
        payload = teleport.process_jwt(teleport_jwt, config)
        roles = payload.get("roles", [])
        user = payload.get("username")
        
        teleport_data = f"User: {user}<br>Roles: {roles}"
        
    else:
        teleport_data = "No Teleport JWT found. Are you accessing this service through Teleport?"
    
    return f"This is a URL decryption service. Use the /decrypt endpoint to decrypt data.<br>{teleport_data}"


if __name__ == "__main__":
    if not config.get("port"):
        config["port"] = 5000
    if not config.get("host"):
        config["host"] = "127.0.0.1"
    app.run(debug=True, port=config["port"], host=config["host"])
