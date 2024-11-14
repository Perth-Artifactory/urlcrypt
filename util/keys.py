import rsa
import base64
import json

# Typing imports
from rsa.key import PrivateKey, PublicKey


def generate_keys() -> tuple:
    """Generate a public and private key pair"""
    
    pubkey, privkey = rsa.newkeys(nbits=4096)

    return pubkey.save_pkcs1(format="PEM"), privkey.save_pkcs1(format="PEM")


def save_keys(pubkey, privkey) -> bool:
    """Save the public and private keys to files"""
    
    with open("public.pem", mode="wb") as publicfile:
        publicfile.write(pubkey)
    with open("private.pem", mode="wb") as privatefile:
        privatefile.write(privkey)
    return True


def load_keys() -> tuple[PublicKey, PrivateKey]:
    """Load the public and private keys from files"""
    
    with open("public.pem", mode="rb") as publicfile:
        pubkeydata = publicfile.read()
    with open("private.pem", mode="rb") as privatefile:
        privkeydata = privatefile.read()
    pubkey = rsa.PublicKey.load_pkcs1(pubkeydata)
    privkey = rsa.PrivateKey.load_pkcs1(privkeydata)

    return pubkey, privkey


def load_public_key() -> PublicKey:
    """Load just the public key from a file"""
    with open("public.pem", mode="rb") as publicfile:
        pubkeydata = publicfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(pubkeydata)

    return pubkey


def decrypt(data: str) -> dict:
    """Decrypt data that has been encrypted by urlcrypt"""
    
    privkey = load_keys()[1]

    # Decode the base64 encoded data
    decoded_data: bytes = base64.urlsafe_b64decode(data.encode("ascii"))

    # Decrypt the data
    decrypted_data = rsa.decrypt(crypto=decoded_data, priv_key=privkey)

    # Decode the decrypted data
    decrypted_data = decrypted_data.decode("ascii")

    # For some reason the string is surrounded by b''
    decrypted_data = decrypted_data[2:-1]

    # Convert the decrypted data to a dictionary
    decrypted_dict = json.loads(decrypted_data)

    return decrypted_dict
