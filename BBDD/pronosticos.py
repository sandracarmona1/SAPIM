import mysql.connector
import pandas as pd
import datetime
import calendar

# from secreto import *
from BBDD.secreto import *

class Pronostico():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def datosPedidos(self, desde, hasta):
        mycursor =self.mydb.cursor()
        sql = "SELECT fecha_ped, SUM(cantidad_ped) FROM pedido WHERE fecha_ped BETWEEN %s AND %s GROUP BY fecha_ped"
        mycursor.execute(sql,(desde, hasta))
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult, columns=["fecha_ped","cantidad_ped"])
        df["fecha_ped"] = pd.to_datetime(df["fecha_ped"])
        df.set_index("fecha_ped", inplace=True)
        ultima_fecha = max(df.index)
        # ultimo_dia_mes = calendar.monthrange(ultima_fecha.year, ultima_fecha.month)[1]
        inicio = min(df.index)
        # fin = ultima_fecha.replace(day=ultimo_dia_mes)
        index = pd.date_range(start=inicio, end=ultima_fecha, freq="D")
        df = df.reindex(index)
        df = df.fillna(0)
        df["cantidad_ped"] = df["cantidad_ped"].astype(float)
        return df
