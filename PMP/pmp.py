import math 
class PMP:
    def __init__(self, pronosticos, pedidos, inventario_inicial, lote):
        self.pronosticos = pronosticos
        self.pedidos = pedidos
        self.inventario_inicial = inventario_inicial
        self.lote = lote

    def planear(self):
        inventario_inicial = []
        inventario_inicial.insert(0,self.inventario_inicial)
        inventario_final = []
        MPS = []
        i = 0
        while i < len(self.pronosticos):
            demanda = max(self.pronosticos[i],self.pedidos[i])
            if demanda > inventario_inicial[i]:
                k = math.ceil((demanda - inventario_inicial[i])/self.lote)
                MPS.insert(i,self.lote*k)
                
            else:
                MPS.insert(i,0)

            inventario_final.insert(i, MPS[i] + inventario_inicial[i] - demanda)
            inventario_inicial.insert(i+1,inventario_final[i])

            i=i+1
        
        self.MPS = MPS
        self.inventario_final = inventario_final[-1]

        return MPS 




