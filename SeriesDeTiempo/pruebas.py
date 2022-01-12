# -*- coding: utf-8 -*-

import numpy as np
import scipy.stats as sct
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
import base64
from io import BytesIO

class QQPlot():
    def __init__(self, data, alfa):
        self.gui = False
        self.alfa = alfa
        self.data = data.to_frame()
        self.data = self.data[self.data["residual"].notna()]
        self.data = self.data.sort_values(["residual"])
        self.data["i"] = np.arange(1, len(self.data)+1).astype(int)
        self.data.set_index("i",inplace=True)
        
        self.data["Q"] = np.nan
        if len(self.data)<=10:
            i=1
            while i<=len(self.data):
                self.data["Q"][i] = ( i - (3/8) ) / ( len(self.data) + (1/4) )
                i = i + 1
        else:
            i=1
            while i<=len(self.data):
                self.data["Q"][i] = ( i - (1/2) ) / len(self.data)
                i = i + 1
                
        self.data["Z"] = self.data["Q"].apply(sct.norm.ppf)   
        
    def __repr__(self):
        self.graficar()
        return (
        "Gráfico QQ Plot " + "\n"
        )
    
    def graficar(self, titulo="", xlabel="", ylabel=""):
        """Gráfico QQ-Plot\n
        titulo: Título de la gráfica\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""
        
        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()
        
        
        a, b = np.polyfit(self.data["Z"], self.data["residual"], deg=1)
        y_est = a * self.data["Z"] + b
        
        
        sr = ((self.data["Z"] - y_est)**2).sum() / ( len(self.data) -2 )
        
        y_err = sct.t.ppf(self.alfa/2, len(self.data)-2) *  (
                                                        sr *
                                                        (
                                                            ( 1/len(self.data["Z"]) ) + 
                                                            ( self.data["Z"]**2 / ((self.data["Z"]**2).sum()) )
                                                        )
                                                     )**0.5
 
        # Linea de regresión
        ax.plot(self.data["Z"], y_est, '-', color='tab:red')
        
        # Área de intervalo
        ax.fill_between(self.data["Z"], y_est - y_err, y_est + y_err, alpha=0.2)
        
        # Puntos 
        ax.plot(self.data["Z"],self.data["residual"],"o")

        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("QQ-Plot")
        if xlabel != "":
            ax.set_xlabel(xlabel)
        else:
            ax.set_xlabel("Z")
        if ylabel != "":
            ax.set_ylabel(ylabel)
        else:
            ax.set_ylabel("residuales")

        ax.grid(linestyle=":")
        
        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data
        
class DurbinWatson:
    def __init__(self, data):
        self.data = data.to_frame()
        self.data.rename(columns={"residual":"et"},inplace=True)
        self.data = self.data[self.data["et"].notna()]
        self.data["i"] = np.arange(1, len(self.data)+1).astype(int)
        self.data.set_index("i",inplace=True)
        
        self.data["et-1"]=self.data["et"].shift()
        
        self.data["(et - et-1)^2"] = (self.data["et"] - self.data["et-1"])**2
        
        self.data["et^2"] = self.data["et"]**2
        
        self.dw = self.data["(et - et-1)^2"].sum() / self.data["et^2"].sum()
        
    def __repr__(self):
        return (
        "Estadístico de Durbin-Watson" + "\n" +
        str(self.dw) + "\n" +
        "Cantidad de datos: " + str(len(self.data))
        
        )

class Levene:
    def __init__(self, data, alfa, L):
        
        self.alfa = alfa
        
        self.data = data
        
        self.data = self.data.drop([0])


        # self.data = data.to_frame()
        
        N = len(data)-1
        Ni = L
        
        k = N / L
        
        self.data["i"] = np.nan
        self.data["Yi."] = np.nan
        
        
        a=0; i = 1
        while i<=k:
            self.data["i"][a:a+L] = i
            self.data["Yi."][a:a+L] = self.data["yt"][a:a+L].mean()
            
            a = a + L
            i = i + 1
        
        self.data["i"] = self.data["i"].astype(int)
        
        self.data["Zij"] = abs( self.data["yt"] - self.data["Yi."] )
        
        self.data["Zi."] = np.nan
        
        a=0
        while a<N:
            self.data["Zi."][a:a+L] = self.data["Zij"][a:a+L].mean()
            
            a = a + L

        Zmedia = self.data["Zij"].mean()
        
        
        
        j=1; sumaNum = 0
        while j<=N:
            sumaNum = sumaNum + Ni * ( self.data["Zi."][j] - Zmedia )**2
            j = j + L
            
        j=1; sumaDen = 0
        while j<=N:
            sumaDen = sumaDen + ( self.data["Zij"][j] - self.data["Zi."][j] )**2
            j = j + 1
        
        self.W = ( ( N-k ) / ( k-1 ) ) * ( sumaNum / sumaDen )
        
        self.gl1 = k-1
        self.gl2 = N-k
        
        self.p_valor = 1 - sct.f.cdf(self.W,self.gl1,self.gl2)
        
        
        
    def __repr__(self):
        
        if self.p_valor > (self.alfa):
            resultado = "Se aprueba la hipotesis nula (H₀)"
        else:
            resultado = "NO se aprueba la hipotesis nula (H₀)"
        
        
        return (
        "PRUEBA DE LEVENE" + "\n\n" +
        "H₀: Las varianzas son homocedásticas, es decir son iguales\n" +  
        "H₁: Las varianzas son heterocedásticas, es decir no son iguales\n\n" +
        "W: " + str(self.W) + "\tgl1: " + str(self.gl1) + "\tgl2: " + str(self.gl2) + "\tSig: " + str(round(self.p_valor,4)) + "\n\n" +
        str(resultado)
        
        )
        