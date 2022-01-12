# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.figure import Figure
import base64
from io import BytesIO

class Autocorrelacion:
    def __init__(self, data, n):
        self.dataOriginal = data
        self.n = n

        self.media = data["yt"].mean()

        self.data = pd.DataFrame(columns=["k","FAC", "FACP"])
        self.gui = False

        k=0
        while k<=n:
            ytk = data["yt"].shift(-k)
            r = ((data["yt"] - self.media) * (ytk - self.media)).sum() / ((data["yt"] - self.media) ** 2).sum()

            self.data = self.data.append({"k":int(k), "FAC": r}, ignore_index=True)
            k = k + 1

        self.data["k"] = self.data["k"].astype(int)
        self.data.set_index("k",inplace = True)
        self.data["FACP"] = np.nan

        # self.data["FACP"][1] = self.data["FAC"][1]

        fac = self.data["FAC"]
        facp = np.empty((n+1,n+1,))
        facp[:] = np.nan

        def r(k,j):
            if not np.isnan(facp[k][j]):
                # print("PASA POR AQUÍ")
                resultado = facp[k][j]
                return resultado

            elif k == j:
                j = 1; sumaNum = 0; sumaDen = 0
                while j <= k-1:
                    sumaNum = sumaNum + ( r(k-1,j) * fac[k-j] )
                    sumaDen = sumaDen + ( r(k-1,j) * fac[j] )
                    j = j + 1
                resultado = ( fac[k] - sumaNum ) / ( 1 - sumaDen )
                facp[k][j] = resultado
                return resultado
            else:
                resultado = r(k-1,j) - ( r(k,k) * r(k-1,k-j) )
                facp[k][j] = resultado
                return resultado

        i = 1
        while i <= n:
            self.data["FACP"][i] = r(i,i)
            i = i + 1


        self.fac = FAC(self.data["FAC"],self.dataOriginal)
        self.facp = FACP(self.data["FACP"])

    def __repr__(self):
        return (
        "FUNCIÓN DE AUTOCORRELACIÓN\n" +
        str(self.data)
        )

    def graficar(self,titulo=""):
        """Grafíca la serie de tiempo\n
        titulo: Título de la gráfica"""

        if not self.gui:
            fig, axs = plt.subplots(2, 1, dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            axs = fig.subplots(2, 1)

        axs[0].stem(self.data.index, self.data["FAC"])
        axs[1].stem(self.data.index, self.data["FACP"])
        if titulo!="":
            axs[0].set_title(titulo)
        else:
            axs[0].set_title("FUNCIONES DE AUTOCORRELACIÓN")

        # axs[0].set_xlabel("k")
        axs[0].set_ylabel("FAC")

        axs[1].set_xlabel("k")
        axs[1].set_ylabel("FACP")

        axs[0].grid(linestyle=":")
        axs[1].grid(linestyle=":")

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

class FAC:
    def __init__(self, data, dataOriginal):

        self.data = data
        self.dataOriginal = dataOriginal
        self.gui = False

    def graficar(self,titulo=""):
        """Grafíca la autocrrelación simple\n
        titulo: Título de la gráfica"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.stem(self.data.index, self.data)

        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("FUNCIÓN DE AUTOCORRELACIÓN SIMPLE")

        ax.set_xlabel("k")
        ax.set_ylabel("FAC")

        ax.grid(linestyle=":")

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

    def k(self,k=3):
        """k: desviaciones para la autocorrelación"""
        return FACk(self.dataOriginal, k=k)

    def __repr__(self):
        return (
        "FUNCIÓN DE AUTOCORRELACIÓN SIMPLE\n" +
        str(self.data)
        )

class FACP:
    def __init__(self, data):
        self.gui = False
        self.data = data

    def graficar(self,titulo=""):
        """Grafíca la autocorrelación parcial\n
        titulo: Título de la gráfica"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.stem(self.data.index, self.data)

        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("FUNCIÓN DE AUTOCORRELACIÓN PARCIAL")

        ax.set_xlabel("k")
        ax.set_ylabel("FACP")

        ax.grid(linestyle=":")

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

    def k(self,k=3):
        """k: desviaciones para la autocorrelación"""
        return self.data[k]

    def __repr__(self):
        return (
        "FUNCIÓN DE AUTOCORRELACIÓN PARCIAL\n" +
        str(self.data)
        )

class FACk:
    def __init__(self, data, k):

        self.gui = False
        self.data = data
        self.k = k

        self.media = self.data["yt"].mean()

        self.data["yt+k"] = self.data["yt"].shift(-k)
        self.data["num"] = (self.data["yt"] - self.media) * (self.data["yt+k"] - self.media)
        self.data["den"] = (self.data["yt"] - self.media) ** 2

        self.mediaNum = self.data["num"].sum()
        self.mediaDen = self.data["den"].sum()

        self.r = self.mediaNum / self.mediaDen

    def __repr__(self):
        return (
        "FUNCIÓN DE AUTOCORRELACIÓN SIMPLE PARA K = " + str(self.k) + "\n"+
        "r = " + str(self.r) + "\n" +
        str(self.data)
        )

    def graficar(self,titulo=""):
        """Grafíca la serie de tiempo\n
        titulo: Título de la gráfica"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.scatter(self.data["yt"],self.data["yt+k"])
        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("FUNCIÓN DE AUTOCORRELACIÓN SIMPLE PARA K = " + str(self.k))

        ax.set_xlabel("yt")
        ax.set_ylabel("yt+k")

        ax.grid(linestyle=":")
        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data
