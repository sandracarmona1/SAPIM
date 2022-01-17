import mysql.connector
import pandas as pd
from BBDD.secreto import *
import datetime

class Produccion():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def cantidadTipoFecha(self, id_prod, fecha_ini, fecha_fin):
        mycursor =self.mydb.cursor()
        sql = "SELECT fecha_ped, SUM(cantidad_ped) FROM pedido WHERE id_silla = %s AND fecha_ped BETWEEN %s AND %s GROUP BY fecha_ped"
        mycursor.execute(sql,(id_prod, fecha_ini, fecha_fin))
        myresult = mycursor.fetchall()

        fecha_ini = datetime.datetime.strptime(fecha_ini, "%Y-%m-%d")
        fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")

        df = pd.DataFrame(myresult, columns=["fecha_ped","cantidad_ped"])
        df["fecha_ped"] = pd.to_datetime(df["fecha_ped"])
        df.set_index("fecha_ped", inplace=True)
        index = pd.date_range(start=fecha_ini, end=fecha_fin, freq="D")
        df = df.reindex(index)
        df = df.fillna(0)
        df["cantidad_ped"] = df["cantidad_ped"].astype(float)



        return df["cantidad_ped"].to_list()

    def tiposSillas(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id_silla FROM tipo_silla")
        myresult = mycursor.fetchall()
        return myresult

    def inventarioSilla(self, id_silla):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT cantidad_inv FROM inventario WHERE id_silla = %s", (id_silla,))
        myresult = mycursor.fetchall()
        myresult = myresult[0][0]
        return myresult
