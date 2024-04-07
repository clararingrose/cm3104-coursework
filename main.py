# to run: source venv/bin/activate
# then:   python3 main.py

from flask import *
from sign import *
from Crypto.PublicKey import RSA
import io
import zipfile

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':
    # save prescription file from user as data
    prescription = request.files['file'].read()

    # create RSA key pair and sign the prescription file
    key = RSA.generate(2048)
    signature = sign(key, prescription)

    # create a zip file and save signature, key, and prescription to it
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        zf.writestr("signature.txt", signature)
        zf.writestr("key.der", key.public_key().export_key())
        zf.writestr("prescription.txt", prescription)
    memory_file.seek(0)

    return send_file(memory_file, download_name='signature.zip')
  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    # import user-uploaded files
    signature = request.files['signature'].read()
    key = RSA.import_key(request.files["key"].read())
    file = request.files['file'].read()

    # verify the signature
    result = verifySignature(key, file, signature)
    return render_template("verify.html", result=result)
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)