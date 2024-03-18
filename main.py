# to run: source venv/bin/activate
# then:   flask run -p 8080
import os
from flask import *
from werkzeug.utils import secure_filename
from sign import *

UPLOAD_FOLDER = "/Users/uni/Documents/Python/cm3104-coursework/files"

app = Flask(__name__)
app.config['UPLOAD_FOLER'] = UPLOAD_FOLDER

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':
    file = request.files['file']
    print("FILE TYPE", type(file))
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    key = generate_key()
    print("KEY", type(key))
    signature = sign(key, file.read())
    print("SIGNATURE", signature)
    return render_template("output.html", signature=signature, key=key)
  return False

@app.route("/verify", methods= ['GET', 'POST'])
def verify():
  if request.method == "POST":
    file = request.files['file'].read()
    signature = request.files['signature'].read()
    key = request.files["key"].read()

    result = verify(key, file, signature)
    return render_template("verify.html", result=result)
  return False

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)