# urlcrypt
Python service that live decrypts URLs sent through it

## Usage

* Generate keys using `generate.py` (first time)
* Encrypt a url using code similar to `example_client`
* Expose listen.py in a secure way (like behind teleport)
* listen.py will decrypt the encrypted url and redirect the browser

## Data format

Data include:

* `url``:str` (required): The URL that should be redirected to if successful
* `roles``:list` (optional): A list of teleport roles that can access the URL. 
  * The role `any` can be used to indicate that the user must access the service via Teleport but doesn't require any particular roles.
  * Omitting this field will disable Teleport checks.
  * The teleport role `access` will always have access to the resource.