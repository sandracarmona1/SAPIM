import BBDD.pronosticos
import SeriesDeTiempo.serie as st
import pandas as pd

class Pronosticar():
    def __init__(self):
        data = BBDD.pronosticos.Pronostico().datosPedidos()
        serie = st.Serie(data, columna = "cantidad_ped")
        mms = serie.mediaMovilSimple(3)
        print(mms)
        
