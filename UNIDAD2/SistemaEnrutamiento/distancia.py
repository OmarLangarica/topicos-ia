import numpy as np
import pandas as pd
from typing import Tuple

# radio de la tierra en km
RADIO_TIERRA = 6371.0

# funcion para calcular la distancia entre dos puntos usando la formula de Haversine
def calcular_distancia_haversine(latitud1: float, longitud1: float, latitud2: float, longitud2: float) -> float:

    # calcula la distancia entre dos puntos lat y lon en KM

    # convertir grados a radianes
    lat1_radiana = np.radians(latitud1)
    lon1_radiana = np.radians(longitud1)
    lat2_radiana = np.radians(latitud2)
    lon2_radiana = np.radians(longitud2)

    # diferencias de coordenadas
    diferencia_lon = lon2_radiana - lon1_radiana
    diferencia_lat = lat2_radiana - lat1_radiana

    # formula de Haversine
    a = np.sin(diferencia_lat / 2.0)**2 + np.cos(lat1_radiana) * np.cos(lat2_radiana) * np.sin(diferencia_lon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # distancia en kilometros
    distancia_en_km = RADIO_TIERRA * c
    
    # retorna la distancia en km
    return distancia_en_km

# funcion para generar la matriz de distancias entre todos los nodos
def crear_matriz_de_distancias(coordenadas: pd.DataFrame) -> np.ndarray:

    # genera la matriz de distancias usando la formula de haversine
    numero_de_nodos = len(coordenadas)
    matriz_distancias = np.zeros((numero_de_nodos, numero_de_nodos))
    
    # extraer las coordenadas como arrays para un acceso mas rapido
    latitudes = coordenadas['Latitud_WGS84'].values
    longitudes = coordenadas['Longitud_WGS84'].values
    
    # llenar la matriz en forma de vector 
    for i in range(numero_de_nodos):
        matriz_distancias[i, :] = calcular_distancia_haversine(latitudes[i], longitudes[i], latitudes, longitudes)

    # retornar la matriz de distancias    
    return matriz_distancias

# funcion para encontrar CD mas cercano a una tienda
def encontrar_cd_mas_cercano(indice_tienda: int, matriz_de_distancias: np.ndarray, indices_cds: list) -> int:
    # encuentra el indice del CD mas cercano a la tienda dada

    # extrae las distancias desde la tienda a todos los CDs
    distancias_a_los_cds = matriz_de_distancias[indice_tienda, indices_cds]
    
    # encuentra el indice del CD con la distancia minima
    indice_local_cd_cercano = np.argmin(distancias_a_los_cds)
    
    # devuelve el indice global del CD
    return indices_cds[indice_local_cd_cercano]