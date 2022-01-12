import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
import pandas as pd
import numpy as np
import copy



class Serie():
    """data: es el DataFrame donde se encuentran los datos\n
       columna: Es la columna del DataFrame que se utilizará como datos"""

    def __init__(self, data, columna=""):

        pd.options.display.max_columns = None

        pd.set_option('mode.chained_assignment', None)
        # super(SeriesDeTiempo, self).__init__()

        # self.data = data[columna: "yt"]


        # self.data.shift()
        # print(data)

        if columna in data.columns:
            self.data = data.rename(columns={columna:"yt"})
        else:
            raise ErrorDeSerie(columna)

        self.data["t"] = np.arange(0,len(self.data))
        self.data["t"] = self.data["t"].astype(int)
        self.data.set_index("t",inplace=True)
        self.data.loc[len(self.data)]=np.nan
        self.data = self.data.shift()
        self.gui = False
        # self.data.index = self.data["t"]

    def __repr__(self):
        return (
        "SERIE DE TIEMPO\n"+
        str(self.data)
        )

    # def __getitem__(self, key):
    #     return self.data[key];

    def naive(self):
        import SeriesDeTiempo.naive
        return SeriesDeTiempo.naive.Naive(self.data[:])

    def mediaMovilSimple(self, longitud=3, desfasada=False):
        """longitud: longitud de la media movil simple, por defecto es 3\n
        desfasada: Si es desfasada o no (True o False), por defecto es False"""
        import SeriesDeTiempo.mediaMovilSimple
        return SeriesDeTiempo.mediaMovilSimple.MediaMovilSimple(self.data[:],longitud,desfasada)

    def mediaMovilDoble(self, longitud=3, desfasada=False):
        """longitud: longitud de ambas medias moviles, por defecto es 3\n
        desfasada: Si es desfasada o no (True o False)"""
        import SeriesDeTiempo.mediaMovilDoble
        return SeriesDeTiempo.mediaMovilDoble.MediaMovilDoble(self.data[:],longitud,desfasada)

    def mediaMovilPonderada(self,ponderaciones):
        """ponderaciones: lista con alfas a ponderar ej: [alfa1,alfa2,alfa3] donde alfa1 > alfa2 > alfa3, etc"""
        import SeriesDeTiempo.mediaMovilPonderada
        return SeriesDeTiempo.mediaMovilPonderada.MediaMovilPonderada(self.data[:],ponderaciones)

    def suavizacionExponencialSimple(self,alfa=0.5):
        """alfa: parámetro alfa del modelo, por defecto es 0.5"""
        import SeriesDeTiempo.suavizacionExponencialSimple
        return SeriesDeTiempo.suavizacionExponencialSimple.SuavizacionExponencialSimple(self.data[:],alfa)

    def mediaMovilDobleConTendencia(self,longitud=3):
        """longitud: longitud de ambas medias moviles, por defecto es 3"""
        import SeriesDeTiempo.mediaMovilDobleConTendencia
        return SeriesDeTiempo.mediaMovilDobleConTendencia.MediaMovilDobleConTendencia(self.data[:],longitud)

    def brown(self, alfa=0.5, M1=None, M2=None):
        """alfa: parámetro alfa del modelo, por defecto es 0.5\n
        M1: Valor inicial de Mat, por defecto es yt para t = 1\n
        M2: Valor inicial de Maat, por defecto es yt para t = 1"""
        import SeriesDeTiempo.brown
        return SeriesDeTiempo.brown.Brown(self.data[:], alfa, M1, M2)

    def holt(self, alfa=0.5, beta=0.5, M=None, T=0):
        """alfa: parámetro alfa del modelo, por defecto es 0.5\n
        beta: parámetro beta del modelo, por defecto es 0.5\n
        M: Valor inicial de Mt, por defecto es yt para t = 1\n
        T: Valor inicial de Tt, por defecto es 0"""
        import SeriesDeTiempo.holt
        return SeriesDeTiempo.holt.Holt(self.data[:], alfa, beta, M, T)

    def holtYWinters(self, metodo, alfa=0.5, beta=0.5, gamma=0.5, L=4):
        """metodo: El método a utilizar "aditivo" para el método aditivo y "multiplicativo" para el método multiplicativo\n
        alfa: parámetro alfa del modelo, por defecto es 0.5\n
        beta: parámetro beta del modelo, por defecto es 0.5\n
        gamma: parámetro gamma del modelo, por defecto es 0.5\n
        L: Longitud de la estacionalidad, por defecto es 4"""
        import SeriesDeTiempo.holtYWinters
        return SeriesDeTiempo.holtYWinters.HoltYWinters(self.data[:], metodo, alfa, beta, gamma, L)

    def descomposicion(self, metodo, L=12):
        """metodo: Es el método a utilizar: "aditivo" para el método aditivo y "multiplicativo" para el método multiplicativo\n
        L: Longitud de la estacionalidad, por defecto es 12"""
        import SeriesDeTiempo.descomposicion
        return SeriesDeTiempo.descomposicion.Descomposicion(self.data[:], metodo, L)

    def diff(self, d=1, n=1):
        """d: Es la cantidad de diferencias que se aplicará a la serie\n
        n: Es el desfase que tendrá las diferencias al aplicarse"""
        nuevo = copy.deepcopy(self)
        i=0
        while i<d:
            nuevo.data["yt"] = (nuevo.data["yt"] - nuevo.data["yt"].shift(n)).shift(-n)
            i = i + 1
        nuevo.data = nuevo.data.dropna()
        nuevo.data.loc[0] = [np.nan]
        nuevo.data = nuevo.data.sort_index()
        return nuevo

    def ln(self):
        nuevo = copy.deepcopy(self)
        nuevo.data["yt"] = np.log(nuevo.data["yt"])

        return nuevo

    def autocorrelacion(self, n=16):
        """n: cantidad de autocorrelaciones"""
        import SeriesDeTiempo.autocorrelacion
        return SeriesDeTiempo.autocorrelacion.Autocorrelacion(self.data[:],n=n)

    def graficar(self,titulo="", xlabel="", ylabel="", tendencia=False):
        """Grafíca la serie de tiempo\n
        titulo: Título de la gráfica\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.plot(self.data["yt"],label="yt")
        if titulo!="":
            ax.set_title(titulo)
        if xlabel != "":
            ax.set_xlabel(xlabel)
        if ylabel != "":
            ax.set_ylabel(ylabel)

        if tendencia:
            a, b = np.polyfit(self.data.index[np.invert(np.isnan(self.data["yt"]))],
                              self.data["yt"][np.invert(np.isnan(self.data["yt"]))],
                              deg=1)
            y_est = a * self.data.index[np.invert(np.isnan(self.data["yt"]))] + b
            ax.plot(self.data.index[np.invert(np.isnan(self.data["yt"]))],y_est, label="tendencia lineal")

        ax.grid(linestyle=":")
        ax.legend()

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data


    def cajasEstacionalidad(self, ciclo=4,comienzo=1,titulo="",xlabel="",ylabel="",grilla=True):
        """Muestra un gráfico de cajas de la serie en ciclos\n
        ciclo: Ciclos en que se agrupará los datos, por defecto es 4\n
        titulo: Título de la gráfica\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y\n
        grilla: Grilla de gráfica (True o False), por defecto True"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        t=comienzo
        data = []
        while t<ciclo+comienzo:
            data.append(self.data["yt"][t::ciclo])
            t = t+1
        ax.boxplot(data)

        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("DIAGRAMA DE CAJAS-ESTACIONALIDAD")
        if xlabel != "":
            ax.set_xlabel(xlabel)

        if ylabel != "":
            ax.set_ylabel(ylabel)

        if grilla:
            ax.grid(linestyle=":")

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data


    def cajas(self, L=4,comienzo=1,titulo="",xlabel="",ylabel="",grilla=True):
        """Muestra un gráfico de cajas de la serie en ciclos\n
        L: Periodos en que se agrupará los datos\n
        titulo: Título de la gráfica\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y\n
        grilla: Grilla de gráfica (True o False), por defecto True"""


        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()


        t=comienzo
        data = []
        while t<len(self.data):
            data.append(self.data["yt"][t:t+L])
            t = t + L
        ax.boxplot(data)

        if titulo!="":
            ax.set_title(titulo)
        else:
            ax.set_title("DIAGRAMA DE CAJAS")
        if xlabel != "":
            ax.set_xlabel(xlabel)

        if ylabel != "":
            ax.set_ylabel(ylabel)

        if grilla:
            ax.grid(linestyle=":")

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data


    def levene(self, alfa=0.05, L=4):
        import SeriesDeTiempo.pruebas
        return SeriesDeTiempo.pruebas.Levene(self.data[:], alfa=alfa, L=L)

class ErrorDeMetodo(Exception):
    def __init__(self, valor, modelo):
        self.valor = valor
        self.modelo = modelo

    def __str__(self):
        return "PABLEX: Error de método, '" + str(self.valor) + "' no es un método válido para el MODELO " + self.modelo + "."

class ErrorDeSerie(Exception):
    def __init__(self, columna):
        self.columna = columna

    def __str__(self):
        return "PABLEX: La columna '" + str(self.columna) + "' no existe en el DataFrame."


class Modelo:

    def __init__(self):
        self.prop = "asd"
        self.gui = False

    def graficar(self,titulo="", xlabel="", ylabel=""):
        """Grafíca la serie de tiempo con el modelo\n
        titulo: Título de la gráfica, por defecto es el nombre del modelo\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()

        ax.plot(self.data["yt"],label="yt")
        ax.plot(self.data["Ft"],label="Ft")
        if titulo=="":
            ax.set_title("MODELO "+self.modelo)
        else:
            ax.set_title(titulo)
        if xlabel != "":
            ax.set_xlabel(xlabel)

        if ylabel != "":
            ax.set_ylabel(ylabel)


        ax.grid(linestyle=":")
        ax.legend()

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

    def calcularErrores(self):
        self.data["residual"] = self.data["yt"] - self.data["Ft"]
        # self.data["|e|"] = abs(self.data["residual"])
        self.errores = Errores(self.data, self.modelo)
        self.residual = Residual(self.data["residual"],self.modelo)
        
    def pronosticar(self, p=1, t=None):
        """Pronostica la serie de tiempo p periodos por delante\n
        p: cantidad de periodos a pronosticar, por defecto es 1.\n
        t: valor de t desde donde comenzará el pronóstico, por defecto comienza luego del último dato"""
        return self.pronosticarMetodo(p,t)





class Errores():
    """Muestra los errores de un modelo de pronóstico"""

    def __init__(self, data, modelo):
        self.mse = (data["residual"]**2).mean()
        self.rmse = pow(self.mse,0.5)
        self.mad = (abs(data["residual"])).mean()
        self.mape = abs( data["residual"] / data["yt"] ).mean()
        yt = pow((data["yt"]**2).mean(),0.5)
        ft = pow((data["Ft"]**2).mean(),0.5)
        self.u_theil = self.rmse / ( yt + ft )

        self.modelo = modelo


    def __repr__(self):
        return (
        "ERRORES MODELO "+self.modelo+"\n"
        "MAD:\t\t" + str(self.mad) + "\n"
        "MSE:\t\t" + str(self.mse) + "\n"
        "RMSE:\t\t" + str(pow(self.mse,0.5)) + "\n"
        "MAPE:\t\t" + str(self.mape * 100) + "%\n"
        "U-THEIL:\t" + str(self.u_theil)
        )

class Residual():
    def __init__(self, data, modelo):
        self.data = data;
        self.modelo = modelo
        self.gui = False

    def __repr__(self):
        return (
        "RESIDUAL DEL "+self.modelo+"\n"+
        str(self.data)
        )

    def graficar(self,titulo="", xlabel="", ylabel=""):
        """Grafíca el residual del modelo\n
        titulo: Título de la gráfica, por defecto es el nombre del modelo\n
        xlabel: Título del eje x\n
        ylabel: Título del eje y"""

        if not self.gui:
            fig, ax = plt.subplots(dpi=300, figsize=(9.6,5.4))
        else:
            fig = Figure(dpi=300, figsize=(9.6,5.4))
            ax = fig.subplots()


        ax.plot(self.data,label="residual")
        # plt.axhline(y=0, linestyle="dashed")

        if titulo == "":
            ax.set_title("RESIDUAL DEL MODELO DE "+self.modelo)
        else:
            ax.set_title(titulo)

        if xlabel != "":
            ax.set_xlabel(xlabel)

        if ylabel != "":
            ax.set_ylabel(ylabel)

        ax.grid()

        ax.legend()

        if not self.gui:
            plt.show()
        else:
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return data

    def qqPlot(self, alfa=0.05):
        """Genera la gráfica QQ Plot\n
            alfa: nivel de significación del intervalo, por defecto es 0.05"""
        import SeriesDeTiempo.pruebas
        return SeriesDeTiempo.pruebas.QQPlot(self.data[:], alfa)

    def durbinWatson(self):
        """Estadístico de Durbin-Watson"""
        import SeriesDeTiempo.pruebas
        return SeriesDeTiempo.pruebas.DurbinWatson(self.data[:])
