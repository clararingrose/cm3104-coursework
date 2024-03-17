from setuptools import debug 
from fileinput import filename
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return("Congratulations, it's a web app!")

@app.route("/form")
def form():
  return render_template("form.html")


if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
