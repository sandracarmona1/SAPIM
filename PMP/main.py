import pmp
pronosticos = [800,900,1200,1500,900,700,600,800]
pedidos = [900,1200,1300,800,1100,600,900,1000]
ii = 500
lote = 1400

planificacion = pmp.PMP(pronosticos,pedidos,ii,lote)
print(planificacion.planear())

print(planificacion.inventario_final)
