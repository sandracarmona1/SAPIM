import mysql.connector

from BBDD.secreto import *

class Vendedores():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
    def getVendedores(self):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT nombre_ven, apellido_ven, id_ven FROM vendedor")
        myresult = mycursor.fetchall()
        return myresult

    def nuevoTrabajador(self,nombre,apellido,numero,usuario,contraseña,direccion):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO `fwweimib_sapim`.`vendedor` (`nombre_ven`, `apellido_ven`, `numero_ven`, `usuario_ven`, `contraseña_ven`, `direccion_ven`, `tipo_ven`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nombre, apellido, numero,usuario,contraseña,direccion,"Vendedor")
        mycursor.execute(sql, val)
        self.mydb.commit()

    def getVendedor(self,id):
        mycursor =self.mydb.cursor()
        sql= "SELECT nombre_ven, apellido_ven, numero_ven, usuario_ven, contraseña_ven, direccion_ven, id_ven FROM vendedor WHERE id_ven=%s"
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        return myresult

    def eliminarTrabajador(self, id):
        mycursor =self.mydb.cursor()
        sql= "DELETE FROM vendedor WHERE id_ven=%s"
        val = (id,)
        mycursor.execute(sql,val)
        self.mydb.commit()
