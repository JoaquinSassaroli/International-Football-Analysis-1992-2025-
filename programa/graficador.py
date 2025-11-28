import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.ticker as ticker

class Graficador:
    #clase para generar y guardar gráficos
    
    def __init__(self, carpeta = "graficos"):
        self._carpeta = carpeta
        os.makedirs(carpeta, exist_ok=True)
        
        self._colores_top3 = {
            "Argentina": "blue",
            "Spain": "red",
            "Brazil": "green",
            "default": "gray" 
        }

    def graficar_partidos_por_anio(self, serie):
        #grafica la cantidad de partidos jugados por año usando un grafico de barras, 
        
        plt.figure(figsize=(14, 6))
        
        plt.bar(serie.index, serie.values, color='skyblue') 
        
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        plt.title("Partidos por Año (1992-2025) - Conteo Anual")
        plt.xlabel("Año")
        plt.ylabel("Cantidad de Partidos")
        plt.xticks(serie.index, rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        ruta = os.path.join(self._carpeta, "partidos_por_anio_barras.png")
        plt.savefig(ruta, bbox_inches="tight")
        plt.close()
        return ruta

    def graficar_victorias_paises(self, df, paises):
        #grafica las victorias anuales de argentina, españa y brasil usando un grafico de lineas conectadas
        
        plt.figure(figsize=(12, 6))
        
        for p in paises:
            color = self._colores_top3.get(p, self._colores_top3["default"])
            plt.plot(df.index, df[p], label=p, color=color, marker='o') 
        
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        plt.title("Victorias por Año - Argentina, España y Brasil")
        plt.xlabel("Año")
        plt.ylabel("Victorias")
        plt.legend()
        plt.grid(axis="both", linestyle="--", alpha=0.7)
        
        ruta = os.path.join(self._carpeta, "victorias_top3_lineas.png")
        plt.savefig(ruta, bbox_inches="tight")
        plt.close()
        return ruta

    def graficar_argentina_porcentajes(self, estadisticas_total, estadisticas_recientes):
        #grafica dos gráficos de torta para la comparativa de Argentina.
        
        etiquetas = ["Victorias", "Empates", "Derrotas"]
        colores = ["#2ca02c", "#1f77b4", "#d62728"]
        
        ganados_t = float(estadisticas_total.get("ganados", 0.0)); empatados_t = float(estadisticas_total.get("empatados", 0.0)); perdidos_t = float(estadisticas_total.get("perdidos", 0.0)); total_t = ganados_t + empatados_t + perdidos_t
        valores_t = [0.0, 0.0, 0.0]
        if total_t > 0.0:
            valores_t = [(ganados_t / total_t) * 100.0, (empatados_t / total_t) * 100.0, (perdidos_t / total_t) * 100.0]
        
        ganados_r = float(estadisticas_recientes.get("ganados", 0.0)); empatados_r = float(estadisticas_recientes.get("empatados", 0.0)); perdidos_r = float(estadisticas_recientes.get("perdidos", 0.0)); total_r = ganados_r + empatados_r + perdidos_r
        valores_r = [0.0, 0.0, 0.0]
        if total_r > 0.0:
            valores_r = [(ganados_r / total_r) * 100.0, (empatados_r / total_r) * 100.0, (perdidos_r / total_r) * 100.0]

        #creación de subplots (las dos tortas)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

        ax1.pie(valores_t, labels=etiquetas, autopct="%1.1f%%", colors=colores, startangle=90)
        ax1.set_title(f"Argentina: % Resultados (1992-2025)\nTotal Partidos: {int(total_t)}")
        ax1.axis("equal")

        ax2.pie(valores_r, labels=etiquetas, autopct="%1.1f%%", colors=colores, startangle=90)
        ax2.set_title(f"Argentina: % Resultados (2020-2025)\nTotal Partidos: {int(total_r)}")
        ax2.axis("equal")
        
        plt.suptitle("Comparación de Rendimiento de Argentina por Período", fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
        
        ruta = os.path.join(self._carpeta, "argentina_porcentajes_comparativa.png")
        plt.savefig(ruta)
        plt.close()
        return ruta