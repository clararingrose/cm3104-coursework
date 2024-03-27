from sign import *
from Crypto.PublicKey import RSA


# generate private key pair

key = RSA.generate(2048)

print(type(key))
print(key)


file = open("static/files/prescription.txt", "rb").read()
print(type(file))

signature = sign(key, file)

# export public key

with open("static/files/key.der", "wb") as f:
    f.write(key.public_key().export_key())

# export signature

with open("static/files/signature.txt", "wb") as f:
    f.write(signature)

# read public key
newkey = open("static/files/key.der", "r")
pubkey = RSA.import_key(newkey.read())
print()

# read signature
sig = open("static/files/signature.txt", "rb").read()

print(pubkey)
print(type(pubkey))

print("VERIFY")
verifySignature (pubkey, file, sig)