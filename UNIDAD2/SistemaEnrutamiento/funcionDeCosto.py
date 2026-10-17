import numpy as np
from typing import List

# definimos variable solucion como una lista de rutas
TipoSolucion = List[List[int]]

def calcular_costo_total_de_solucion(
    solucion_actual: TipoSolucion,
    _matriz_de_distancias: np.ndarray,
    matriz_de_costos: np.ndarray
) -> float:
    # La matriz de costos ya contiene el costo en USD de cada tramo.
    _ = _matriz_de_distancias

    # inicializamos costo total
    costo_total = 0.0
    
    # iterar sobre cada ruta en la solucion
    for una_ruta in solucion_actual:
        # Una ruta valida debe tener al menos: CD -> Tienda X -> CD
        if len(una_ruta) < 2:
            continue

        # iterar sobre todos los tramos (i a j) de la ruta
        for i in range(len(una_ruta) - 1):
            nodo_de_inicio = una_ruta[i]
            nodo_de_fin = una_ruta[i+1]

            # La matriz de distancias se conserva en la firma porque se usa
            # para construir y modificar las rutas, pero no escala el costo.
            costo_total += matriz_de_costos[nodo_de_inicio, nodo_de_fin]
        
    return costo_total