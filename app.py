from flask import Flask, session, request, url_for, render_template, redirect
from BBDD.acceso import Acceso
from BBDD.vendedores import Vendedores

app = Flask(__name__)

app.secret_key = "asdasd"

@app.route("/")
def index():
    if 'id' in session:
        return render_template("administrador/index.html", usuario = session["id"])
    else:
        return redirect(url_for('acceso'))

@app.route("/acceso")
def acceso():
    return render_template("acceso.html")

@app.route("/administracion-pedidos")
def adm_pedidos():
    return render_template("administrador/administracion-pedidos.html")

@app.route("/cronograma-produccion")
def cro_produccion():
    return render_template("administrador/cronograma-produccion.html")

# V E N D E D O R E S

@app.route("/vendedores")
def lista_vendedores():
    vendedores = Vendedores()

    return render_template("administrador/vendedores.html", vendedores = vendedores.getVendedores())

@app.route("/datos-vendedores/<id>")
def datos_vendedor(id):
    vendedor = Vendedores()

    return render_template("administrador/datos-vendedores.html", vendedor = vendedor.getVendedor(id)[0])

@app.route("/agregar-trabajador/")
def nuevo_trabajador():
    return render_template("administrador/agregar-trabajador.html")

@app.route("/agregar-trabajador/", methods=['POST', 'GET'])
def agregar_trabajador():
    if request.method == 'POST':
        nuevo = Vendedores()
        nuevo.nuevoTrabajador(
            request.form['nombres'],
            request.form['apellidos'],
            request.form['numero'],
            request.form['usuario'],
            request.form['contrasenia'],
            request.form['direccion']
        )
    return redirect(url_for('lista_vendedores'))


@app.route("/informe-demandas")
def inf_demanda():
    return render_template("administrador/informe-demandas.html")

@app.route("/agregar-trabajador")
def agr_trabajador():
    return render_template("administrador/agregar-trabajador.html")

@app.route("/eliminar-trabajador/<id>")
def eliminar_trabajador(id):
    eliminacion = Vendedores()
    eliminacion.eliminarTrabajador(id)
    return redirect(url_for('lista_vendedores'))

@app.route("/agregar-otro-trabajador/", methods=['POST', 'GET'])
def agregar_otro_trabajador():
    if request.method == 'POST':
        nuevo = Vendedores()
        nuevo.nuevoTrabajador(
            request.form['nombres'],
            request.form['apellidos'],
            request.form['numero'],
            request.form['usuario'],
            request.form['contrasenia'],
            request.form['direccion']
        )
    return redirect(url_for('agr_trabajador'))

# SESIONES DE USUARIO

@app.route("/dar-acceso", methods=['POST', 'GET'])
def darAcceso():
    if request.method == 'POST':

        acceso = Acceso()
        respuesta = acceso.comprobarAcceso(
            request.form['usuario'],
            request.form['contrasenia']
        )
        if respuesta["acceso"]:
            session["id"] = respuesta["id"]

        return redirect(url_for('index'))


@app.route("/quitar-acceso")
def quitarAcceso():
    session.pop('id', None)
    return redirect(url_for('index'))
