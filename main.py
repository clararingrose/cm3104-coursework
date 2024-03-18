# to run: source venv/bin/activate
# then:   flask run -p 8080
import os
from flask import *
from werkzeug.utils import secure_filename
from sign import *

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
    file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
    
    # create key and save to file
    key = generate_key()
    with open("static/files/key.der", "wb") as f:
      f.write(key.public_key().export_key())

    # create signature and save to file
    signature = sign(key, file.read())
    writeFile(os.path.join(UPLOAD_FOLDER), '/signature.txt', signature)
    
    return render_template("output.html", signature=signature, key=key)
  return render_template("index.html")

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    file = request.files['file'].read()
    signature = request.files['signature'].read()
    key = request.files["key"].read()
    print(key)
    key = RSA.import_key(key)
    print(key)

    result = verifySignature(key, file, signature)
    return render_template("verify.html", result=result)
  return False

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)