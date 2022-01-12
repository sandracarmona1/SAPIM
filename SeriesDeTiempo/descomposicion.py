# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import SeriesDeTiempo.serie
import copy

from matplotlib.figure import Figure
import base64
from io import BytesIO

class Descomposicion(SeriesDeTiempo.serie.Modelo):
    """docstring for Descomposicion."""

    def __init__(self, data, metodo, L):
        self.modelo = "DE DESCOMPOSICIÓN"
        self.data = data
        self.comprobado = False
        self.L = L
        self.metodo = metodo

        # self.data["Mt"] = np.nan
        
        if int(L) % 2 == 0:
            l2 = int(-(L/2))
            self.data["Mt1"] = self.data["yt"].rolling(window=L).mean().shift(l2)
            self.data["Tt"] = self.data["Mt1"].rolling(window=2).mean()
            
        else:
            l2 = round(-(L/2))
            self.data["Tt"] = self.data["yt"].rolling(window=L).mean().shift(l2)
        
        
        if metodo=="aditivo":
            
            self.modelo = self.modelo + " ADITIVO"
            
            self.data["yt-Tt"] = self.data["yt"]-self.data["Tt"]
            
            self.data["St"] = np.nan
            
            t=1
            while (t<=L):
                self.data["St"][t] = self.data["yt-Tt"][t::L].mean()
                t = t + 1
                
            t=1 
            prom = self.data["St"][1:(L+1)].mean()
            while (t<=L):
                self.data["St"][t::L] = self.data["St"][t]-prom
                t = t + 1

            self.data["yt-St"] = self.data["yt"]-self.data["St"]
            
            self.data["Ft"] = self.data["St"]+self.data["Tt"]


            a, b = np.polyfit(self.data.index[self.data["yt-St"].notna()], self.data["yt-St"][self.data["yt-St"].notna()], deg=1)
            self.data["Tt_Reg"] = a * self.data.index + b
            
            self.data["Ft_Reg"] = self.data["Tt_Reg"] + self.data["St"]
            
        elif metodo=="multiplicativo":
            
            self.modelo = self.modelo + " MULTIPLICATIVO"
            
            self.data["yt/Tt"] = self.data["yt"]/self.data["Tt"]
            
            self.data["St"] = np.nan
            
            t=1
            while (t<=L):
                self.data["St"][t] = self.data["yt/Tt"][t::L].mean()
                t = t + 1
                
            t=1 
            prom = self.data["St"][1:(L+1)].mean()
            while (t<=L):
                self.data["St"][t::L] = self.data["St"][t]/prom
                t = t + 1

            self.data["yt/St"] = self.data["yt"]/self.data["St"]
            
            self.data["Ft"] = self.data["St"] * self.data["Tt"]
            
            
            a, b = np.polyfit(self.data.index[self.data["yt/St"].notna()], self.data["yt/St"][self.data["yt/St"].notna()], deg=1)
            self.data["Tt_Reg"] = a * self.data.index + b
            
            self.data["Ft_Reg"] = self.data["Tt_Reg"] * self.data["St"]
            
        else:
            raise SeriesDeTiempo.serie.ErrorDeMetodo(metodo,self.modelo)
        
        self.regA = a; self.regB = b

        self.tendencia = Tendencia(self.data["Tt"], self.modelo)
        self.estacionalidad = Estacionalidad(self.data["St"][1:L+1], self.modelo)
        self.calcularErrores()
        
        self.data["residual_Reg"] = self.data["yt"] - self.data["Ft_Reg"]
        self.residualReg = SeriesDeTiempo.serie.Residual(self.data["residual_Reg"],self.modelo)
        
    def __repr__(self):
        return (
        "MODELO "+self.modelo+"\n"+
        str(self.data)
        )

            
    def pronosticarMetodo(self, p, t0):
        
        nuevo = copy.deepcopy(self)
               
        if t0==None:
            t0 = len(nuevo.data)
        

        t = t0
        while t < int(t0) + int(p):
            if (nuevo.data.index != t).all():
                nuevo.data.loc[t]=np.nan
                
            ts = t%self.L
            if ts == 0:
                ts = self.L
            
            nuevo.data["St"][t] = nuevo.data["St"][ts]
                  
            if self.metodo == "aditivo":
                nuevo.data["Ft_Reg"][t] = (self.regA * nuevo.data.index[t] + self.regB) + nuevo.data["St"][t]
            elif self.metodo == "multiplicativo":
                nuevo.data["Ft_Reg"][t] = (self.regA * nuevo.data.index[t] + self.regB) * nuevo.data["St"][t]
            else:
                raise SeriesDeTiempo.serie.ErrorDeMetodo(self.metodo,self.modelo)
            
            t = t + 1
        
        nuevo.calcularErrores()
        self.data["residual_Reg"] = self.data["yt"] - self.data["Ft_Reg"]
        self.residualReg = SeriesDeTiempo.serie.Residual(self.data["residual_Reg"],self.modelo)
        return nuevo
        
        
        
        
        
        
        
        
            
class Tendencia:
    def __init__(self, data, modelo):
        self.data = data;
        self.modelo = modelo
    
    def __repr__(self):
        return (
        "TENDENCIA DEL "+self.modelo+"\n"+
        str(self.data)
        )
    
    def graficar(self, titulo="", xlabel="", ylabel=""):
        """Grafica la tendencia descompuesta de la serie de tiempo\n
        titulo: Título de la gráfica, por defecto es el nombre del modelo\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""
        
        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.plot(self.data,label="Tt")
        if titulo == "":
            ax.set_title("TENDENCIA DEL MODELO DE "+self.modelo)
        else:
            ax.set_title(titulo)
            
        if xlabel != "":
            ax.set_xlabel(xlabel)
          
        if ylabel != "":
            ax.set_ylabel(ylabel)
            
        ax.legend()
        ax.grid(linestyle=":")
        
        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

class Estacionalidad:
    def __init__(self, data, modelo):
        self.data = data;
        self.modelo = modelo
    
    def __repr__(self):
        return (
        "ESTACIONALIDAD DEL "+self.modelo+"\n"+
        str(self.data)
        )
    
    def graficar(self, titulo="", xlabel="", ylabel=""):
        """Grafica la estacionalidad descompuesta de la serie de tiempo\n
        titulo: Título de la gráfica, por defecto es el nombre del modelo\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""
        
        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.plot(self.data,label="St")
        
        if titulo == "":
            ax.set_title("ESTACIONALIDAD DEL MODELO "+self.modelo)
        else:
            ax.set_title(titulo)
            
        if xlabel != "":
            ax.set_xlabel(xlabel)
          
        if ylabel != "":
            ax.set_ylabel(ylabel)
            
        ax.legend()
        ax.grid(linestyle=":")
        
        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data
