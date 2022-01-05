from flask import Flask, session, request, url_for, render_template, redirect
from BBDD.acceso import Acceso
from BBDD.vendedores import Vendedores
from BBDD.pedidos import Pedidos
import json

app = Flask(__name__)

app.secret_key = "asdasd"

@app.route("/")
def index():
    if 'id' in session:
        if session["tipo"] == "Administrador":
            return render_template("administrador/index.html", usuario = session["id"])

        elif session["tipo"] == "Vendedor":
            return render_template("vendedor/index.html", usuario = session["id"])

        elif session["tipo"] == "Trabajador":
            return render_template("trabajador/index.html", usuario = session["id"])

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
def informeDeDemandas():
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

# P E D I D O S

# from controladores.pedidos import *

@app.route("/hacer-pedido")
def hacerPedidoVista():
    pedido = Pedidos()
    tiposDeProductos = pedido.tiposDeProductos()
    tiposDeTelas = pedido.tiposDeTelas()
    return render_template("vendedor/hacer-pedido.html", tiposDeProductos = tiposDeProductos, tiposDeTelas = tiposDeTelas)

@app.route("/hallar-colores/", methods=['POST', 'GET'])
def hallarColores():
    if request.method == 'POST':
        pedidoColores = Pedidos()
        colores = pedidoColores.coloresDeTela(request.form['idTipoDeTela'])
        return json.dumps(colores)

@app.route("/realizar-pedido/", methods=['POST', 'GET'])
def realizarPedido():
    if request.method == 'POST':
        nuevoPedido = Pedidos()
        nuevoPedido.pedir(session["id"],
            request.form['idTipoDeProducto'],
            request.form['idTipoDeTela'],
            request.form['idColorDeTela'],
            request.form['cantidad'],
            request.form['fecha'],
            "0")
    return redirect(url_for('historialPedidos'))

@app.route("/historial-de-pedidos/")
def historialPedidos():
    id_ven = session["id"]
    pedidos = Pedidos()
    historial = pedidos.historial(id_ven)
    return render_template("vendedor/historial-de-pedidos.html", historial=historial)

@app.route("/cancelar-pedido/", methods=['POST', 'GET'])
def cancelarPedido():
    if request.method == 'POST':
        cancelacion = Pedidos()
        cancelacion.cancelar(request.form['id_pedido'])
        return redirect(url_for('historialPedidos'))

@app.route("/pedidos-para-peudccion/")
def pedidosParaProduccion():
    pedidos = Pedidos()
    historial = pedidos.pedidosProd()
    return render_template("administrador/pedidos-para-produccion.html", historial=historial)


# S E S I O N E S   D E   U S U A R I O

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
            session["tipo"] = respuesta["tipo"]

    return redirect(url_for('index'))



@app.route("/quitar-acceso")
def quitarAcceso():
    session.pop('id', None)
    return redirect(url_for('index'))
