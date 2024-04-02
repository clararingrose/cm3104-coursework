# to run: source venv/bin/activate
# then:   python3 main.py
import os
from flask import *
from sign import *
from Crypto.PublicKey import RSA

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

    print(type(signature))
    print(signature)
    # print(signature.decode('ascii'))
    
    return render_template("output2.html", signature=signature.decode(), key=key.public_key().export_key().decode())
  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    # import user-uploaded files
    signature = request.files['signature'].read()
    key = RSA.import_key(request.files["key"].read())
    file = request.files['file'].read()

    result = verifySignature(key, file, signature)
    return render_template("verify.html", result=result)
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)