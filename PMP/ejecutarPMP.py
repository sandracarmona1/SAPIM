from BBDD.produccion import *
from Pronosticos.pronosticar import *
from PMP.pmp import *
import datetime
import calendar

class ejecutarPMP(object):
    """docstring for ejecutarPMP."""

    def __init__(self, semana):
        calendario = calendar.Calendar(firstweekday=6)

        mes_actual = int(datetime.datetime.today().strftime("%m"))
        anio_actual = int(datetime.datetime.today().strftime("%Y"))

        dias = calendario.itermonthdates(anio_actual, mes_actual)
        dias = [i for i in dias]

        semanas_ini = dias[0::7]
        semanas_fin = dias[6::7]


        # fecha_ini = semanas_ini[semana].strftime("%Y-%m-%d")
        # fecha_fin = semanas_fin[semana].strftime("%Y-%m-%d")

        fecha_ini = dias[0].strftime("%Y-%m-%d")
        fecha_fin = dias[-1].strftime("%Y-%m-%d")

        print(fecha_ini)
        print(fecha_fin)

        # fecha_ini = "2022-01-05"
        # fecha_fin = "2022-01-11"

        consultaProd = Produccion()
        consultaPron = Pronosticar()

        tiposProductos = consultaProd.tiposSillas()

        # print(consulta.cantidadTipoFecha(1,fecha_ini,fecha_fin))
    def calcular():

        for id in tiposProductos:
            id = id[0]
            print(id)
            pedidos = consultaProd.cantidadTipoFecha(id, fecha_ini, fecha_fin)
            print(pedidos)
            inventario = consultaProd.inventarioSilla(id)
            print(inventario)
            pronostico = consultaPron.hallarPronostico(fecha_ini, fecha_fin)["Ft"]
            print(pronostico)
            planificacion = PMP(pronostico, pedidos, inventario, 2)
            print(planificacion.planear())
            print("\n")

asd = ejecutarPMP(1)
