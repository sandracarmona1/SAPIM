import mysql.connector

from BBDD.secreto import *
class Pedidos():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def tiposDeProductos(self):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT id_silla, nombre_silla, foto_silla FROM tipo_silla")
        myresult = mycursor.fetchall()
        return myresult

    def tiposDeTelas(self):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT id_tela,nombre_tela,foto_tela FROM tipo_tela")
        myresult = mycursor.fetchall()
        return myresult

    def coloresDeTela(self,id_tela):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT id_color, nombre_color,foto_color FROM tela_color WHERE id_tela="+str(id_tela))
        myresult = mycursor.fetchall()
        return myresult

    def pedir(self, id_ven, id_silla, id_tela,id_color, cantidad_ped, fecha_ped, confirmacion_ped ):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO `fwweimib_sapim`.`pedido` (`id_ven`, `id_silla`, `id_tela`, `id_color`, `cantidad_ped`, `fecha_ped`,`confirmacion_ped`) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val = (id_ven, id_silla, id_tela, id_color, cantidad_ped, fecha_ped, confirmacion_ped)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def historial(self, id_ven):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT id_pedido, (SELECT nombre_silla FROM tipo_silla WHERE id_silla=pedido.id_silla), (SELECT nombre_tela FROM tipo_tela WHERE id_tela=pedido.id_tela), (SELECT nombre_color FROM tela_color WHERE id_color=pedido.id_color), detalle_ped, fecha_ped, estado_proc FROM pedido WHERE id_ven="+str(id_ven)+" AND confirmacion_ped='0'")
        myresult = mycursor.fetchall()
        return myresult

    def cancelar(self, id_pedido):
        mycursor =self.mydb.cursor()
        sql= "DELETE FROM `fwweimib_sapim`.`pedido` WHERE  `id_pedido`=%s"
        val = (id_pedido,)
        mycursor.execute(sql,val)
        self.mydb.commit()

    def pedidosProd(self):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT id_pedido, (SELECT nombre_silla FROM tipo_silla WHERE id_silla=pedido.id_silla), (SELECT nombre_tela FROM tipo_tela WHERE id_tela=pedido.id_tela), (SELECT nombre_color FROM tela_color WHERE id_color=pedido.id_color), detalle_ped, fecha_ped, estado_proc FROM pedido WHERE confirmacion_ped='1'")
        myresult = mycursor.fetchall()
        return myresult
