# urlcrypt
Python service that live decrypts URLs sent through it

## Usage

* Generate keys using `generate.py` (first time)
* Encrypt a url using code similar to `example_client`
* Expose listen.py in a secure way (like behind teleport)
* listen.py will decrypt the encrypted url and redirect the browser