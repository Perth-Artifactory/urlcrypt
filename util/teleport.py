import base64
import json
from pprint import pprint
import requests
from jose import jwt, jwk

def add_padding(base64_string: str) -> str:
    return base64_string + '=' * (-len(base64_string) % 4)

def process_jwt(jwt_header: str, config: dict) -> tuple[str, str, str]:
    # Retrieve the jwks from Teleport
    jwks_url = f"{config['teleport_base']}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    jwks_key = jwks["keys"][0]
    
    # Split the JWT into its header, payload, and signature
    parts = jwt_header.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT")
    header_b64, payload_b64, signature_b64 = parts
    
    # Decode the header and payload
    payload_json = base64.urlsafe_b64decode(add_padding(payload_b64)).decode()
    
    # Convert the header and payload to dictionaries
    payload = json.loads(payload_json)
    
    # Verify the JWT signature
    public_key = jwk.construct(jwks_key)
    message = f'{header_b64}.{payload_b64}'
    signature = base64.urlsafe_b64decode(add_padding(signature_b64))
    
    if not public_key.verify(message.encode(), signature):
        raise ValueError("Invalid JWT signature")
    
    return payload

def check_access(require: list, have: list):
    """Check whether the user has access to the resource"""
    
    # The access roll overwrites all other rolls
    if "access" in have:
        return True
    
    # Used when a resource should be available to everyone with teleport access
    if "any" in require:
        return True
    
    for role in have:
        if role in require:
            return True
        
    return False
    