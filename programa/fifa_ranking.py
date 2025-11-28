import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

class ScraperFifa:
    #clase para obtener el top del ranking fifa actual desde transfermarkt.
    
    def __init__(self, url = "https://www.transfermarkt.com.ar/statistik/weltrangliste"):
        self._url = url
        self._top10 = pd.DataFrame(columns=["posicion", "pais", "puntos"])
    
    @property
    def top10(self):
        return self._top10
    
    @top10.setter
    def top10(self, valor):
        if not isinstance(valor, pd.DataFrame):
            raise TypeError("El valor asignado debe ser un DataFrame")
        self._top10 = valor
    
    def obtener_ranking(self, cantidad = 10):
        #realiza el scraping y actualiza la propiedad top10
        datos = []
        try:
            resp = requests.get(
                self._url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
            )
            resp.raise_for_status()
            sopa = BeautifulSoup(resp.text, "html.parser")
            datos = self._obtener_transfermarkt(sopa, cantidad)
        except Exception:
            datos = []
        
        if datos:
            df = pd.DataFrame(datos)
            if "pais" not in df.columns:
                df["pais"] = None
            if "puntos" not in df.columns:
                df["puntos"] = None
                
            df["pais"] = df["pais"].astype(str).str.replace(r"[A-Z]{3}$", "", regex=True).str.strip()
            df["puntos"] = pd.to_numeric(df["puntos"], errors="coerce")
            
            df = df.dropna(subset=["pais"]).sort_values("puntos", ascending=False).reset_index(drop=True)
            df["posicion"] = df.index + 1
            df_final = df.head(cantidad).copy()
        else:
            df_final = pd.DataFrame(columns=["posicion", "pais", "puntos"]).head(cantidad)
        
        self.top10 = df_final
        return self.top10
    
    def _obtener_transfermarkt(self, sopa, cantidad):
        #lógica de parsing de Transfermarkt
        cont = sopa.find("div", id="yw1")
        tabla = cont.find("table", class_="items") if cont else sopa.find("table", class_="items")
        if not tabla:
            return []
        
        headers_idx = {"pos": 0, "pais": 1, "puntos": None}
        thead = tabla.find("thead")
        if thead:
            ths = thead.find_all("th")
            textos = [th.get_text(strip=True).lower() for th in ths]
            for i, t in enumerate(textos):
                if t in ("#", "clas."):
                    headers_idx["pos"] = i
                if ("país" in t) or ("pais" in t):
                    headers_idx["pais"] = i
                if ("puntos" in t) or ("pkte" in t):
                    headers_idx["puntos"] = i
        if headers_idx["puntos"] is None:
            headers_idx["puntos"] = 6
        
        cuerpo = tabla.find("tbody") or tabla
        filas = cuerpo.find_all("tr")
        datos = []
        for tr in filas:
            tds = tr.find_all("td")
            if tds:
                def texto_td(idx):
                    if idx is None or idx >= len(tds):
                        return ""
                    cell = tds[idx]
                    txt = cell.get_text(" ", strip=True)
                    if not txt:
                        a = cell.find("a")
                        if a:
                            txt = a.get_text(strip=True)
                    return txt
                    
                pais = texto_td(headers_idx["pais"]).strip()
                puntos_txt = texto_td(headers_idx["puntos"]) or ""
                puntos_txt = "".join(c for c in puntos_txt if c.isdigit() or c in ",.")
                try:
                    puntos = float(puntos_txt.replace(".", "").replace(",", ".")) if puntos_txt else None
                except Exception:
                    puntos = None
                    
                if pais:
                    datos.append({"posicion": None, "pais": pais, "puntos": puntos})
        
        datos = [d for d in datos if d.get("pais")]
        datos.sort(key=lambda x: (x["puntos"] is None, -(x["puntos"] or 0)))
        for i, d in enumerate(datos):
            if i < cantidad:
                d["posicion"] = i + 1
            else:
                return datos[:cantidad]
        
        return datos[:cantidad]