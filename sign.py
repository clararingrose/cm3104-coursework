# main source : https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_pss.html

from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def sign(key, document):
  # print("SIGN KEY:", key)
  h = SHA256.new(document)
  signature = pss.new(key).sign(h)
  # print(type(signature))
  # print(signature)
  return signature

def verifySignature(key, document, signature):
  # print("VERIFY KEY:", key.publickey())
  h = SHA256.new(document)
  verifier = pss.new(key.publickey())
  try:
      verifier.verify(h, signature)
      print("The signature is authentic.")
      return "The signature is authentic."
  except (ValueError):
      print("The signature is not authentic.")
      return "The signature is not authentic."

def writeFile(filePath, fileName, data):
   file = open(filePath + fileName, "wb")
   file.write(data)
   file.close()

#testing
# newkey =  RSA.generate(3072)
# newdoc = open('prescription.txt', 'rb').read()
# sig = sign(newkey, newdoc)

# verifySignature(newkey, newdoc, sig)