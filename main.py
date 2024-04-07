# to run: source venv/bin/activate
# then:   python3 main.py

from flask import *
from sign import *
from Crypto.PublicKey import RSA
import io
import zipfile

pwd = b'VLWy^CGD#4p2#L26s4x^B8kdnsQ2pX'

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':

    # if the user does not upload a private key, generate one for them
    if not request.files['privkey']:
      # save prescription file from user as data
      prescription = request.files['file'].read()

      # create RSA key pair and sign the prescription file
      privkey = RSA.generate(3072)
      signature = sign(privkey, prescription)

      # create a zip file and save signature, private key, public key, and prescription to it
      memory_file = io.BytesIO()
      with zipfile.ZipFile(memory_file, 'w') as zf:
          zf.writestr("signature.txt", signature)
          zf.writestr("privatekey.der", privkey.export_key(passphrase=pwd, pkcs=8, protection='PBKDF2WithHMAC-SHA512AndAES256-CBC', prot_params={'iteration_count':131072}))
          zf.writestr("pubkey.der", privkey.public_key().export_key())
          zf.writestr("prescription.txt", prescription)
      memory_file.seek(0)

      return send_file(memory_file, download_name='signature.zip')
    
    else:
      # save prescription file and private RSA key from user as data
      prescription = request.files['file'].read()
      privkey = RSA.import_key(request.files['privkey'].read(), pwd)

      # sign the prescription file with the user's private key
      signature = sign(privkey, prescription)

      # create a zip file and save signature, key, and prescription to it
      memory_file = io.BytesIO()
      with zipfile.ZipFile(memory_file, 'w') as zf:
          zf.writestr("signature.txt", signature)
          zf.writestr("pubkey.der", privkey.public_key().export_key())
          zf.writestr("prescription.txt", prescription)
      memory_file.seek(0)

      return send_file(memory_file, download_name='signature.zip')

  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    # import user-uploaded files
    signature = request.files['signature'].read()
    pubkey = RSA.import_key(request.files['pubkey'].read())
    file = request.files['file'].read()

    # verify the signature
    result = verifySignature(pubkey, file, signature)
    return render_template("index.html", result=result)
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)