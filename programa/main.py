from carga_datos import CargadorDatos
from analizador import Analizador
from graficador import Graficador
from fifa_ranking import ScraperFifa 
import os
import sys
import pandas as pd

#definición de la ruta del CSV
RUTA_CSV = os.path.join(
    os.path.dirname(__file__), 
    "../dataset/Resultados(1992-2025).csv"
)

#top 3 fijo para el gráfico de líneas
TOP3_FIJO = ["Argentina", "Spain", "Brazil"] 

RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_GRAFICOS = os.path.join(RUTA_BASE, "graficos")


def inicializar_datos():
    #carga datos y realiza los análisis necesarios para generar los gráficos
    try:
        cargador = CargadorDatos(RUTA_CSV)
        cargador.cargar()
        datos = cargador.datos
        
        analizador = Analizador(datos)
        
        #partidos por año
        partidos_anio = analizador.partidos_por_anio()
        
        #estadísticas de Argentina(Total)
        estadisticas_arg_total = analizador.estadisticas_pais_periodo("Argentina", 1992, 2025)
        
        #estadísticas de Argentina(Reciente)
        estadisticas_arg_reciente = analizador.estadisticas_pais_periodo("Argentina", 2020, 2025)
        
        #victorias del top 3 fijo 
        victorias_top3 = analizador.victorias_por_pais(TOP3_FIJO)
        
        #generación de gráficos
        graficador = Graficador(RUTA_GRAFICOS) 
        rutas = {}
        
        rutas["partidos_anio"] = graficador.graficar_partidos_por_anio(partidos_anio)
        rutas["victorias_top3"] = graficador.graficar_victorias_paises(victorias_top3, TOP3_FIJO)
        rutas["argentina_porcentajes"] = graficador.graficar_argentina_porcentajes(
            estadisticas_arg_total, estadisticas_arg_reciente
        )
        
        return rutas

    except Exception as e:
        print(f"Error al inicializar o generar datos: {e}")
        return None

def mostrar_imagen(ruta):
    #muestra la imagen generada
    if not os.path.exists(ruta):
        print(f"Archivo no encontrado")
        return
    
    #se intenta abrir el archivo con la aplicación predeterminada del sistema
    try:
        if sys.platform == "win32":
            os.startfile(ruta)
        elif sys.platform == "darwin":
            os.system(f"open {ruta}")
        else:
            os.system(f"xdg-open {ruta}")
        print(f"Gráfico '{os.path.basename(ruta)}' abierto en pantalla.")
    except Exception:
        print(f"No se pudo abrir el gráfico")

def mostrar_menu(rutas, error_opcion=False):
    #muestra el menú de opciones y gestiona la elección
    
    if error_opcion:
        print("Opción inválida.")
        
    print("\n--- Menú de Gráficos ---")
    print("1. Partidos por Año (Gráfico de Barras)")
    print("2. Victorias Anuales de Argentina, España y Brasil (Gráfico de Líneas)")
    print("3. Argentina: % Resultados (Comparativa de Gráficos de Torta)")
    print("4. Salir")
    
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        mostrar_imagen(rutas["partidos_anio"])
        mostrar_menu(rutas) 
    elif opcion == "2":
        mostrar_imagen(rutas["victorias_top3"]) 
        mostrar_menu(rutas) 
    elif opcion == "3":
        mostrar_imagen(rutas["argentina_porcentajes"])
        mostrar_menu(rutas) 
    elif opcion == "4":
        return
    else:
        mostrar_menu(rutas, error_opcion=True)


if __name__ == "__main__":
    rutas_graficos = inicializar_datos()
    
    if rutas_graficos is not None:
        mostrar_menu(rutas_graficos)
    else:
        print("No se pudieron inicializar los datos")