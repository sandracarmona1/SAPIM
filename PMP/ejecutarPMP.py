from BBDD.produccion import *
from Pronosticos.pronosticar import *
from PMP.pmp import *
import datetime
import calendar
import pandas as pd


def ponerFormato(fecha):
    return fecha.strftime("%d/%m/%Y")


class ejecutarPMP(object):
    """docstring for ejecutarPMP."""

    def __init__(self):
        calendario = calendar.Calendar(firstweekday=6)

        mes_actual = int(datetime.datetime.today().strftime("%m"))
        anio_actual = int(datetime.datetime.today().strftime("%Y"))

        dias = calendario.itermonthdates(anio_actual, mes_actual)
        dias = [i for i in dias]

        self.semanas_ini = dias[0::7]
        self.semanas_fin = dias[6::7]

        # fecha_ini = semanas_ini[semana].strftime("%Y-%m-%d")
        # fecha_fin = semanas_fin[semana].strftime("%Y-%m-%d")

        self.fecha_ini = dias[0].strftime("%Y-%m-%d")
        self.fecha_fin = dias[-1].strftime("%Y-%m-%d")

        # fecha_ini = "2022-01-05"
        # fecha_fin = "2022-01-11"

        # print(consulta.cantidadTipoFecha(1,fecha_ini,fecha_fin))

    def calcular(self):

        df = pd.DataFrame()
        index = pd.date_range(start=self.fecha_ini,
                              end=self.fecha_fin, freq="D")
        df["fechas"] = index
        df["fechas"] = df["fechas"].apply(ponerFormato)
        # df = df.reindex(index)
        df.set_index("fechas", inplace=True)

        consultaProd = Produccion()
        consultaPron = Pronosticar()

        tiposProductos = consultaProd.tiposSillas()

        for id in tiposProductos:

            id = id[0]
            print(id)
            pedidos = consultaProd.cantidadTipoFecha(
                id, self.fecha_ini, self.fecha_fin)
            inventario = consultaProd.inventarioSilla(id)
            pronostico = consultaPron.hallarPronostico(
                self.fecha_ini, self.fecha_fin)["Ft"]

            planificacion = PMP(pronostico, pedidos, inventario, 2)
            df[id] = planificacion.planear()

        print(df)
        t = 0
        semanas = []
        while t < len(self.semanas_ini):
            semanas.append(df[self.semanas_ini[t].strftime(
                "%d/%m/%Y"):self.semanas_fin[t].strftime("%d/%m/%Y")].to_dict("index"))
            t = t + 1

        return semanas[0]


print(ejecutarPMP().calcular())
