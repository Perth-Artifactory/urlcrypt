from util import keys
import os

print("This script will generate a new pair of RSA keys.")

# Check for existing keys
if os.path.exists("public.pem") or os.path.exists("private.pem"):
    print("WARNING: Keys already exist in this directory.")
    print(
        "WARNING: IF YOU DO THIS ON A PRODUCTION IMPLEMENTATION YOU WILL BREAK THINGS"
    )
else:
    print("No keys found in this directory.")

choice = input("Do you want to generate new keys? (y/N): ")

if choice.lower() == "y":
    print("Generating keys...")
    pubkey, privkey = keys.generate_keys()
    # back up the old keys if they exist
    if os.path.exists("public.pem"):
        print("Backing up old public key to public.pem.bak")
        os.rename("public.pem", "public.pem.bak")
    if os.path.exists("private.pem"):
        print("Backing up old private key to private.pem.bak")
        os.rename("private.pem", "private.pem.bak")
    keys.save_keys(pubkey, privkey)
    print("Keys generated and saved to public.pem and private.pem.")
