from util import keys
from pprint import pprint

data = input("Enter the encrypted URL: ")

# Strip everything before the ?data= part
if "?data=" in data:
    data = data.split("?data=")[1]

data = keys.decrypt(data)

pprint(data)
