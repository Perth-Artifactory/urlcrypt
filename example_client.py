import rsa
import json
from pprint import pprint

from util import client

# Load config
with open("config.json", mode="r") as f:
    config: dict = json.load(f)


print("This script will encrypt a URL using the public key.")
data: dict = {"url": "https://google.com/", "roles": []}
pprint(data)

print("Encrypting data...")
url = client.encrypt(data, config)
print("URL:", url)
