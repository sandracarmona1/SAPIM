# -*- coding: utf-8 -*-

import numpy as np
import SeriesDeTiempo.serie
import copy

class MediaMovilDobleConTendencia(SeriesDeTiempo.serie.Modelo):
    """docstring for MediaMovilDobleConTendencia."""

    def __init__(self, data,longitud):
        self.modelo = "MEDIA MÓVIL DOBLE CON TENDENCIA"
        self.data = data
        self.comprobado = True

        self.data["Mts"] = self.data["yt"].rolling(window=longitud).mean()
        self.data["Mtss"] = self.data["Mts"].rolling(window=longitud).mean()       
        
        
        self.data["at"] = np.nan
        self.data["bt"] = np.nan
        self.data["Ft"] = np.nan
        
        t = ( longitud * 2 ) - 1
        while ( t<len(self.data) ):
            self.data["at"][t] = 2 * self.data["Mts"][t] - self.data["Mtss"][t]
            self.data["bt"][t] = ( 2/(longitud-1) ) * ( self.data["Mts"][t] - self.data["Mtss"][t] )
            
            if t > (longitud*2)-1:
                self.data["Ft"][t] = self.data["at"][t-1] + self.data["bt"][t-1]
            
            t = t + 1
            
        self.calcularErrores()

    def __repr__(self):
        return (
        "MODELO "+self.modelo+"\n"+
        str(self.data)
        )


    def pronosticarMetodo(self, n, t):
        
        nuevo = copy.deepcopy(self)
        
        
        if t!=None:
            ti=t
        else:
            long = len(nuevo.data)
            ti=long
            t=long
        
        while ti < t + n:
            if (nuevo.data.index != ti).all():
                nuevo.data.loc[ti]=np.nan
                
            nuevo.data["Ft"][ti]= nuevo.data["at"][t-1] + nuevo.data["bt"][t-1] * ( ti - t + 1 )
            
            ti = ti + 1
        
        nuevo.calcularErrores()
        return nuevo