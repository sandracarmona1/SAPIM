# -*- coding: utf-8 -*-

import EOQA.eoqa

K = [10, 5, 15]
D = [2, 4, 4]
h = [0.3, 0.1, 0.2]
a = [1, 1, 1]

inventario = EOQA.eoqa.EOQA(D, K, h, a, 25)
inventario.optimizar(10000)







import PMP.pmp

pronosticos = [800,900,1200,1500,900,700,600,800]
pedidos = [900,1200,1300,800,1100,600,900,1000]
ii = 500
lote = 1400

planificacion = PMP.pmp.PMP(pronosticos, pedidos, ii, lote)

planificacion.planear()


planificacion.inventario_final





