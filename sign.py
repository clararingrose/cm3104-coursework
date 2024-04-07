# main source : https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_pss.html

from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def sign(key, document):
  h = SHA256.new(document)
  print(h)
  signature = pss.new(key).sign(h)
  return signature

def verifySignature(key, document, signature):
  h = SHA256.new(document)
  verifier = pss.new(key)
  try:
      verifier.verify(h, signature)
      return "The signature is authentic."
  except (ValueError):
      return "The signature is not authentic."