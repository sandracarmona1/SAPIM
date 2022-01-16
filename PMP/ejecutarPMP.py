from BBDD.produccion import *
import datetime

consulta = Produccion()

fecha_ini = "2022-01-04"
fecha_fin = "2022-01-10"



tiposProductos = consulta.tiposSillas()



# print(consulta.cantidadTipoFecha(1,fecha_ini,fecha_fin))

for id in tiposProductos:
    id = id[0]
    print(id)
    resultados = consulta.cantidadTipoFecha(id,fecha_ini,fecha_fin)
    inventario = consulta.inventarioSilla(id)

    print(resultados)
    for resultado in resultados:





#     id = id + 1
