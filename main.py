# to run: source venv/bin/activate
# then:   flask run -p 8080
import os
from flask import *
from sign import *
from Crypto.PublicKey import RSA

UPLOAD_FOLDER = "/Users/uni/Documents/Python/cm3104-coursework/static/files"

app = Flask(__name__)
app.config['UPLOAD_FOLER'] = UPLOAD_FOLDER

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':
    # save the uploaded data to file
    file = request.files['file']

    # create key and save to file
    key = RSA.generate(2048)
    with open("static/files/key.der", "wb") as f:
      f.write(key.public_key().export_key())

    # create signature and save to file
    signature = sign(key, file.read())
    with open("static/files/signature.txt", "wb") as f:
      f.write(signature)
    
    return render_template("output.html", signature=signature, key=key.public_key())
  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    file = request.files['file'].read()
    # print("FILE", file)
    # print(type(file))
    signature = request.files['signature'].read()
    # print("SIG", signature)
    # print(type(signature))
    key = RSA.import_key(request.files["key"].read())
    # print("PUBLIC KEY", key)
    # print(type(key))

    result = verifySignature(key, file, signature)
    return render_template("verify.html", result=result)
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)