# to run: source venv/bin/activate
# then:   flask run -p 8080

from flask import *
#from werkzeug import secure_filename
from sign import *

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/output", methods = ['GET', 'POST'])
def output():
  if request.method == 'POST':
    file = request.files['file'].read()
    # f.save(secure_filename(f.filename))
    key = generate_key()
    signature = sign(key, file)
    return render_template("output.html", signature=signature, key=key)
  return False

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
