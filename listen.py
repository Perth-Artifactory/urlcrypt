import json

from flask import Flask, jsonify, request, redirect

from util import keys

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

    # Retrieve the URL from the decrypted data
    url = decrypted_data.get("url")

    if not url:
        return jsonify({"error": "No URL found in the decrypted data"}), 400

    # Redirect the client to the URL
    return redirect(url)


@app.route("/", methods=["GET"])
def root_endpoint():
    return jsonify(
        {
            "message": "This is a URL decryption service. Use the /decrypt endpoint to decrypt data."
        }
    )


if __name__ == "__main__":
    if not config["port"]:
        config["port"] = 5000
    if not config["host"]:
        config["host"] = "127.0.0.1"
    app.run(debug=True, port=config["port"], host=config["host"])
