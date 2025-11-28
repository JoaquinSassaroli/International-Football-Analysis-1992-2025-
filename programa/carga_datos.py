import pandas as pd
import numpy as np
from dateutil import parser as parser_fecha

class CargadorDatos:
    #clase que carga y transformar el dataset de partidos internacionales
    
    def __init__(self, ruta_csv):
        self._ruta_csv = ruta_csv
        self._datos = None 
    
    @property
    def datos(self):
        if self._datos is None:
            raise ValueError("Datos no cargados")
        return self._datos
    
    @datos.setter
    def datos(self, valor):
        if not isinstance(valor, pd.DataFrame):
            raise TypeError("El valor debe ser un DataFrame de Pandas")
        self._datos = valor
    
    def cargar(self):
        #lee el CSV y aplica transformaciones
        df = pd.read_csv(
            self._ruta_csv,
            sep=";",
            encoding="latin-1",
            low_memory=False,
            on_bad_lines="skip",
        )
        
        df = df.rename(columns={c: c.strip() for c in df.columns})
        
        #normalizacion
        mapeo = {}
        for col in df.columns:
            c = col.lower()
            if "date" in c:
                mapeo[col] = "fecha"
            elif "home" in c and "team" in c:
                mapeo[col] = "equipo_local"
            elif "away" in c and "team" in c:
                mapeo[col] = "equipo_visitante"
            elif "home" in c and ("score" in c or "goal" in c):
                mapeo[col] = "goles_local"
            elif "away" in c and ("score" in c or "goal" in c):
                mapeo[col] = "goles_visitante"
        
        if mapeo:
            df = df.rename(columns=mapeo)
        
        if "fecha" in df.columns:
            df["fecha"] = df["fecha"].apply(self._parsear_fecha_seguro)
            df["anio"] = df["fecha"].dt.year
        else:
            df["anio"] = np.nan
        
        #conversion de numeros
        for col in ("goles_local", "goles_visitante"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        
        #creacion de columna resultado
        if "goles_local" in df.columns and "goles_visitante" in df.columns:
            df["resultado"] = df.apply(self._resultado_partido, axis=1)
        
        self._datos = df
    
    def _parsear_fecha_seguro(self, valor):
        try:
            return parser_fecha.parse(str(valor), dayfirst=False)
        except Exception:
            return pd.NaT
    
    def _resultado_partido(self, fila):
        if fila["goles_local"] > fila["goles_visitante"]:
            return "local_gana"
        if fila["goles_local"] < fila["goles_visitante"]:
            return "visitante_gana"
        return "empate"
    
    def lista_paises(self):
        df = self.datos
        columnas = []
        if "equipo_local" in df.columns:
            columnas.append("equipo_local")
        if "equipo_visitante" in df.columns:
            columnas.append("equipo_visitante")
        
        if not columnas:
            return []
        
        lista = pd.concat([df[c] for c in columnas]).dropna().unique().tolist()
        return sorted(lista)