from flask import Flask, session, request, url_for, render_template, redirect

app = Flask(__name__)

app.secret_key = "asdasd"

@app.route("/")
def index():
    if 'usuario' in session:
        return render_template("index.html", usuario = session["usuario"])
    else:
        return redirect(url_for('acceso'))

@app.route("/acceso")
def acceso():
    return render_template("acceso.html")

@app.route("/administracion-pedidos")
def adm_pedidos():
    return render_template("administracion-pedidos.html")

@app.route("/cronograma-produccion")
def cro_produccion():
    return render_template("cronograma-produccion.html")

@app.route("/datos-vendedores")
def dat_vendedores():
    return render_template("datos-vendedores.html")

@app.route("/informe-demandas")
def inf_demanda():
    return render_template("informe-demandas.html")

@app.route("/agregar-trabajador")
def agr_trabajador():
    return render_template("agregar-trabajador.html")

# SESIONES DE USUARIO
 
@app.route("/dar-acceso", methods=['POST', 'GET'])
def darAcceso():
    if request.method == 'POST':
        session["usuario"] = request.form['usuario']
        return redirect(url_for('index'))

@app.route("/quitar-acceso")
def quitarAcceso():
    session.pop('usuario', None)
    return redirect(url_for('index'))
