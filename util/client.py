import rsa
import json
import base64


def encrypt(data, config: dict | None = None):  # type: ignore

    if config is None:
        # Load config
        with open("config.json", mode="r") as f:
            config: dict = json.load(f)

    with open("public.pem", mode="rb") as publicfile:
        pubkeydata = publicfile.read()
        public_key = rsa.PublicKey.load_pkcs1(pubkeydata)

    # Prepare the data
    if type(data) == dict:
        data = json.dumps(data)

    data = data.encode("ascii")

    # Encrypt the data
    encrypted_data = rsa.encrypt(message=str(data).encode("ascii"), pub_key=public_key)

    # Encode the data in a url-safe way
    encoded_data = base64.urlsafe_b64encode(encrypted_data).decode("ascii")
    url = f"{config['public_base']}/decrypt?data={encoded_data}"

    return url
