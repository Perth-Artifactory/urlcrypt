import rsa
import base64
from util import keys, client
import json

# Load keys from files
loaded_pubkey, loaded_privkey = keys.load_keys()

# Data to be encrypted
data = {"url": "https://google.com/", "roles": []}

# Encrypt the data
encrypted_data = client.encrypt(data, config={"public_base": "http://example.com"})

# Extract the base64 encoded encrypted data from the URL
encoded_data = encrypted_data.split("?data=")[1]

# Decode and decrypt the data
decrypted_data = keys.decrypt(encoded_data)

print("Original data:", data)
print("Decrypted data:", decrypted_data)
