from BBDD.produccion import *

consulta = Produccion()

fecha_ini = "2022-01-04"
fecha_fin = "2022-01-10"

tiposProductos = consulta.tiposSillas()

# print(consulta.cantidadTipoFecha(1,fecha_ini,fecha_fin))

for id in tiposProductos:
    id = id[0]
    print(id)
    resultados = consulta.cantidadTipoFecha(id,fecha_ini,fecha_fin)
    print(resultados)


    
    
    
#     id = id + 1
