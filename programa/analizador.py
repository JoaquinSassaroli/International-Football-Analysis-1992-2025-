import pandas as pd
import numpy as np

class Analizador:
    #clase que genera estadisticas a partir del dataset
    
    def __init__(self, datos):
        self._df = datos.copy()
    
    def get_df(self):
        return self._df.copy()
    
    def partidos_por_anio(self):
        df_limpio = self._df.dropna(subset=["anio"])
        df_limpio["anio"] = df_limpio["anio"].astype(int) 
        return df_limpio.groupby("anio").size().sort_index()
    
    def victorias_por_pais(self, paises):
        #calcula las victorias por año para una lista de países
        
        df = self._df.dropna(subset=["anio"])
        df["anio"] = df["anio"].astype(int)
        anios = sorted(df["anio"].unique().astype(int))
        tabla = pd.DataFrame(index=anios)
        
        for pais in paises:
            mask_local = (df["equipo_local"] == pais) & (df["resultado"] == "local_gana")
            mask_visit = (df["equipo_visitante"] == pais) & (df["resultado"] == "visitante_gana")
            
            victorias = df.loc[mask_local | mask_visit].groupby("anio").size()
            tabla[pais] = victorias.reindex(anios, fill_value=0)
        
        return tabla
    
    def estadisticas_pais_periodo(self, pais, anio_inicio=1992, anio_fin=2025):
        #calcula las estadísticas para un pais entre 1992 y 2025
        
        df = self._df.copy()
        df = df[(df["anio"] >= anio_inicio) & (df["anio"] <= anio_fin)]
        
        local = df[df["equipo_local"] == pais]
        visitante = df[df["equipo_visitante"] == pais]
        
        total = len(local) + len(visitante)
        
        ganados = len(local[local["resultado"] == "local_gana"]) + len(visitante[visitante["resultado"] == "visitante_gana"])
        
        condicion_participo = (df["equipo_local"] == pais) | (df["equipo_visitante"] == pais)
        empates = len(df[condicion_participo & (df["resultado"] == "empate")])
        
        perdidos = total - ganados - empates
        
        resultado = {
            "partidos_totales": float(total),
            "ganados": float(ganados),
            "empatados": float(empates),
            "perdidos": float(perdidos),
        }
        return resultado