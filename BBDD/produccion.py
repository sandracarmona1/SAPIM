import mysql.connector

from BBDD.secreto import *
class Produccion():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def cantidadTipoFecha(self, id_prod, fecha_ini, fecha_fin):
        mycursor =self.mydb.cursor()
        sql = "SELECT fecha_ped, SUM(cantidad_ped) FROM pedido WHERE id_silla = %s AND fecha_ped BETWEEN %s AND %s GROUP BY fecha_ped"
        mycursor.execute(sql,(id_prod, fecha_ini, fecha_fin))

        myresult = mycursor.fetchall()
        return myresult

    def tiposSillas(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id_silla FROM tipo_silla")
        myresult = mycursor.fetchall()
        return myresult

    def inventarioSilla(self, id_silla):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT cantidad_inv FROM inventario WHERE id_silla = %s", id_silla)
        myresult = mycursor.fetchall()
        return myresult
