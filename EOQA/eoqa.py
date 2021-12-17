# -*- coding: utf-8 -*-

import random

class EOQA:
    """Modelo de EOQ con almacenamiento"""
    def __init__(self, d, k, h, a, area):
        self.d = d
        self.k = k
        self.h = h
        self.a = a
        self.area = area
        
    def f(self, var):
        
        fsuma = 0
        i = 0
        while i < len(var):
            fsuma = fsuma + (self.k[i] * self.d[i]) / var[i] +(self.h[i] * var[i]) / 2
            i = i + 1
        
        return fsuma

    def generar(self, ant):
        
        gen = []
        i = 0
        
        while i < len(ant):
            gen.insert(i, ant[i] + random.randint(-5,5))
            i = i + 1
        
        return gen

    def optimizar(self, n):
        """n: Cantidad de iteraciones a realizar"""
        
        # punto de arranque       
        opt = []
        i = 0
        while i < len(self.a):
            opt.insert(i,1)
            i = i + 1
        
        f_opt = self.f(opt)
        
        i = 0
        while i<n:
            
            var = self.generar(opt)
            
            sumaArea = 0
            proposicion0 = True

            j = 0
            while j<len(var):
                sumaArea = sumaArea + self.a[j]*var[j]
                proposicion0 = proposicion0 and (var[j] >= 0)
                j = j + 1
            
            if (sumaArea <= self.area) and proposicion0:
            
                
                try:
                    f_alt = self.f(var)
                except ZeroDivisionError:
                    pass
                else:
                    if f_alt < f_opt:
                        f_opt = f_alt
                        opt = var
                    
            i = i + 1
            
        self.opt = opt
        
        return opt













    # def graficar(self)
    #     i = 0
    #     while i<n:
            
    #         x, y = generar(x_opt, y_opt)
            
    #         # x = random.randint(0,25)
    #         # y = random.randint(0,25)
            
    #         # Pertenece al dominio?
    #         if a[0]*x + a[1]*y <= 25 and x>=0 and y>=0:
            
    #             try:
    #                 f_alt = f(x,y)
    #             except ZeroDivisionError:
    #                 # print(x,y,"División entre 0")
    #                 pass
    #             else:
                    
    #                 busqueda = busqueda.append({"x": x,
    #                                             "y": y,
    #                                             "f": f_alt},
    #                                             ignore_index=True)

    #                 if f_alt < f_opt:
    #                     f_opt = f_alt
    #                     x_opt = x
    #                     y_opt = y
                
    #                     print(x_opt,y_opt,f_opt)

    #         i = i + 1










        # import matplotlib.pyplot as plt
        # fig, ax = plt.subplots(figsize=(3,3),dpi=300)
        # ax.scatter(busqueda["x"],
        #             busqueda["y"],
        #             c=-busqueda["f"])
        # plt.show()

