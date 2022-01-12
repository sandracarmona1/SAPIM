import BBDD.pronosticos
import SeriesDeTiempo.serie as st
import pandas as pd

class Pronosticar():
    def hallarPronostico(self, desde, hasta):
        data = BBDD.pronosticos.Pronostico().datosPedidos(desde, hasta)
        inicio = data.index[0]
        fin = data.index[-1]
        serie = st.Serie(data, columna = "cantidad_ped")
        mms = serie.mediaMovilSimple(3).data
        mms = mms.drop(mms.index[0])

        index = pd.date_range(start = inicio, end = fin, freq = "D")
        mms["fecha_ped"] = index
        mms = mms.fillna(0)
        resultado = []
        t = 1
        while t < len(mms):
            resultado.append(
                (mms["fecha_ped"][t].strftime("%d/%m/%Y"), mms["yt"][t], mms["Ft"][t])
             )
            t = t + 1


        fechas = []
        t = 1
        while t < len(mms):
            fechas.append(
                str(mms["fecha_ped"][t].strftime("%d/%m/%Y"))
             )
            t = t + 1

        # mms.set_index("fecha_ped",inplace = True)

        # mms = mms.reindex(index)


        return {"resultado": resultado,
            "fechas": fechas,
            "yt": mms["yt"].to_list(),
            "Ft": mms["Ft"].to_list(),}
