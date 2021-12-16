from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/asd")
def asd():
    return "<p>Página ASD</p>"

@app.route("/asd2")
def asd2():
    return "<p>Página ASD2</p>"