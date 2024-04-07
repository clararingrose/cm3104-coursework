# to run: source venv/bin/activate
# then:   python3 main.py

from flask import *
from sign import *
from Crypto.PublicKey import RSA
import random
import io

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':
    # save user-uploaded file as data
    file = request.files['file'].read()

    # create key pair and save public key to file
    key = RSA.generate(2048)
    with open("static/files/key.der", "wb") as f:
      f.write(key.public_key().export_key())

    # create signature and save to file
    signature = sign(key, file)
    with open("static/files/signature.txt", "wb") as f:
      f.write(signature)
    
    return render_template("output.html", signature=signature, key=key.public_key().export_key().decode())
  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    # import user-uploaded files
    signature = request.files['signature'].read()
    print(type(signature))
    key = RSA.import_key(request.files["key"].read())
    file = request.files['file'].read()

    result = verifySignature(key, file, signature)
    return render_template("verify.html", result=result)
  return render_template("index.html")

@app.route('/signature.txt')
def signature():
    """Serves the signature file."""

    with open("static/files/signature.txt", 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='signature.txt',
                     mimetype='text/plain'
               )

@app.route('/key.der')
def key():
    """Serves the public key file."""

    with open("static/files/key.der", 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='key.der',
                     mimetype='text/plain'
               )

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)