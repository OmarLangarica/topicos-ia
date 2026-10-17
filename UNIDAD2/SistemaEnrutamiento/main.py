import json
import re
from pathlib import Path

import pandas as pd

from cargarDatos import cargar_datos_desde_archivos
from recocidoSimulado import ejecutar_recocido_simulado
from funcionDeCosto import TipoSolucion

DIRECTORIO_PROYECTO = Path(__file__).resolve().parent
DIRECTORIO_DATOS = DIRECTORIO_PROYECTO / "Datos"
ARCHIVO_DE_COORDENADAS = DIRECTORIO_DATOS / "datos_distribucion_tiendas.xlsx"
ARCHIVO_DE_DISTANCIAS = DIRECTORIO_DATOS / "matriz_distancias.xlsx"
ARCHIVO_DE_COSTOS = DIRECTORIO_DATOS / "matriz_costos_combustible.xlsx"
ARCHIVO_MAPA_BASE = DIRECTORIO_PROYECTO / "mapa_geoespacial_actualizado.html"
NOMBRE_ARCHIVO_SALIDA_HTML = DIRECTORIO_PROYECTO / "mapa_rutas_optimizadas.html"

# parametros del recocido simulado
TEMPERATURA_INICIAL = 1000.0 
TEMPERATURA_FINAL = 0.1
FACTOR_DE_ENFRIAMIENTO = 0.98
NUMERO_DE_ITERACIONES_POR_TEMPERATURA = 500

def _coordenadas_del_mapa_base(contenido_html: str) -> tuple[str, list[tuple[float, float]]]:
    variable_mapa = re.search(r"var (map_[A-Za-z0-9_]+) = L\.map", contenido_html)
    if variable_mapa is None:
        raise ValueError("No se encontró el objeto de mapa Leaflet en el HTML base.")

    coincidencias = re.findall(
        r"L\.(?:circleMarker|marker)\(\s*\[\s*"
        r"([-+]?\d+(?:\.\d+)?)\s*,\s*([-+]?\d+(?:\.\d+)?)",
        contenido_html,
    )
    if not coincidencias:
        raise ValueError("No se encontraron marcadores con coordenadas en el HTML base.")

    return variable_mapa.group(1), [(float(latitud), float(longitud))
                                    for latitud, longitud in coincidencias]


def generar_mapa_de_rutas(
    coordenadas: pd.DataFrame,
    solucion: TipoSolucion,
    archivo_mapa_base: Path,
    nombre_archivo_html: Path,
) -> None:
    contenido_html = archivo_mapa_base.read_text(encoding="utf-8")
    variable_mapa, coordenadas_mapa = _coordenadas_del_mapa_base(contenido_html)
    if len(coordenadas_mapa) != len(coordenadas):
        raise ValueError(
            f"El mapa base tiene {len(coordenadas_mapa)} nodos y los datos tienen "
            f"{len(coordenadas)} nodos; no es seguro trazar las rutas."
        )

    colores = ["blue", "green", "purple", "orange", "darkred", "cadetblue"]
    capas_rutas = []
    for indice_ruta, una_ruta in enumerate(solucion):
        if len(una_ruta) < 2:
            continue
        puntos = [
            coordenadas_mapa[indice_nodo]
            for indice_nodo in una_ruta
        ]
        nombre_cd = str(coordenadas.loc[una_ruta[0], "Nombre"])
        color = colores[indice_ruta % len(colores)]
        capas_rutas.append(
            f"L.polyline({json.dumps(puntos)}, "
            f"{{color: {json.dumps(color)}, weight: 4, opacity: 0.85}})"
            f".bindPopup({json.dumps(f'Ruta {indice_ruta + 1}: {nombre_cd}')})"
            f".addTo({variable_mapa});"
        )

    bloque_rutas = (
        "\n<script>\n"
        + "\n".join(capas_rutas)
        + "\n</script>\n"
    )
    # El HTML de Folium declara el mapa después de cerrar `body`; las rutas
    # deben agregarse al final para que la variable Leaflet ya exista.
    contenido_html = contenido_html.replace("</html>", bloque_rutas + "</html>", 1)
    nombre_archivo_html.write_text(contenido_html, encoding="utf-8")
    print(f"\nMapa de rutas generado y guardado como '{nombre_archivo_html}'")

# funcion principal
def ejecutar_programa_principal():
    # cargar datos
    dataframe_coordenadas, matriz_de_distancias, matriz_de_costos = cargar_datos_desde_archivos(
        str(ARCHIVO_DE_COORDENADAS),
        str(ARCHIVO_DE_DISTANCIAS),
        str(ARCHIVO_DE_COSTOS),
    )
    
    # ejecuta el recocido simulado
    mejor_solucion_encontrada, costo_final_optimo, _ = ejecutar_recocido_simulado(
        matriz_de_distancias,
        matriz_de_costos,
        temp_inicial=TEMPERATURA_INICIAL,
        temp_final=TEMPERATURA_FINAL,
        factor_enfriamiento=FACTOR_DE_ENFRIAMIENTO,
        iteraciones_por_temp=NUMERO_DE_ITERACIONES_POR_TEMPERATURA
    )
    
    # resultados por consola
    print("\n--- RESULTADOS FINALES DE LA OPTIMIZACIÓN ---")
    print("Costo Final optimo: $" + str.format('{:,.2f}', costo_final_optimo) + " USD")
    print("\n--- RUTAS ÓPTIMAS ENCONTRADAS (CD -> Tiendas -> CD) ---")
    
    for i, una_ruta in enumerate(mejor_solucion_encontrada):
        # mapear los indices de los nodos a sus nombres
        nombres_de_la_ruta = [dataframe_coordenadas.loc[nodo, 'Nombre'] for nodo in una_ruta]
        ruta_en_string = " -> ".join(nombres_de_la_ruta)
        print("Ruta " + str(i+1) + ": " + ruta_en_string)
        
    # generar mapa de rutas
    generar_mapa_de_rutas(
        dataframe_coordenadas,
        mejor_solucion_encontrada,
        ARCHIVO_MAPA_BASE,
        NOMBRE_ARCHIVO_SALIDA_HTML,
    )
    
if __name__ == "__main__":
    ejecutar_programa_principal()