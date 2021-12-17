from flask import Flask, session, request, url_for

app = Flask(__name__)

app.secret_key = "asdasd"

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/asd")
def asd():
    return "<p>Página ASD</p>"

@app.route("/asd2")
def asd2():
    return "<p>Página ASD2</p>"

# SESIONES DE USUARIO

@app.route("/dar-acceso", methods=['POST', 'GET'])
def darAcceso():
    if request.method == 'POST':
        session.clear()
        session["usuario"] = request.form['usuario']
        return redirect(url_for('index'))

@app.route("/quitar-acceso")
def quitarAcceso():
    session.pop('usuario', None)
    return redirect(url_for('index'))
