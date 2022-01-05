import mysql.connector

# from secreto import *
from BBDD.secreto import *

class Acceso():
    def __init__(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def comprobarAcceso(self,usuario,contraseña):
        mycursor = self.mydb.cursor()
        sql = "SELECT id_ven, tipo_ven FROM vendedor WHERE usuario_ven=%s AND contraseña_ven=%s"
        val = (usuario,contraseña)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            acceso=True
            id = myresult[0][0]
            tipo = myresult[0][1]
        else:
            acceso=False
            id = None
            tipo = None

        return {"acceso":acceso, "id":id, "tipo": tipo}
