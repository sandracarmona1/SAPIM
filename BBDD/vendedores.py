import mysql.connector

from secreto import *

class Vendedores():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
    def getVendedores(self):
        mycursor =self.mydb.cursor()
        mycursor.execute("SELECT nombre_ven, apellido_ven FROM vendedor")
        myresult = mycursor.fetchall()
        return myresult
    
    def nuevoVendedor(self,nombre,apellido,numero,usuario,contraseña,direccion):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO `fwweimib_sapim`.`vendedor` (`nombre_ven`, `apellido_ven`, `numero_ven`, `usuario_ven`, `contraseña_ven`, `direccion_ven`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (nombre, apellido, numero,usuario,contraseña,direccion)
        mycursor.execute(sql, val)
        self.mydb.commit()
    
    def getVendedor(self,id):
        mycursor =self.mydb.cursor()
        sql= "SELECT nombre_ven, apellido_ven, numero_ven, usuario_ven,contraseña_ven, direccion_ven FROM vendedor WHERE id_ven=%s"
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        return myresult