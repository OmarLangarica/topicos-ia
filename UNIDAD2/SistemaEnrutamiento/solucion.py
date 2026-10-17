import random
import numpy as np
from typing import List, Tuple
from funcionDeCosto import TipoSolucion
from distancia import encontrar_cd_mas_cercano 

# definimos numero de nodos, CD y tiendas
NUMERO_TOTAL_DE_NODOS = 100
NUMERO_DE_CDS = 10
NUMERO_DE_TIENDAS = 90

# funcion para crear una solucion inicial
def crear_solucion_inicial(matriz_de_distancias: np.ndarray) -> TipoSolucion:

    # crea una solucion inicial asignando cada tienda a su CD mas cercano
    # separar indices de CDs y tiendas
    indices_de_los_cds = list(range(NUMERO_DE_CDS))
    indices_de_las_tiendas = list(range(NUMERO_DE_CDS, NUMERO_TOTAL_DE_NODOS))
    
    # crea una lista de listas para las rutas una para cada CD
    rutas_por_cd = [[] for _ in indices_de_los_cds]
    
    # asignar cada tienda a su CD mas cercano
    for indice_tienda in indices_de_las_tiendas:
        #funcion que encuentra el CD mas cercano a la tienda
        cd_mas_cercano = encontrar_cd_mas_cercano(indice_tienda, matriz_de_distancias, indices_de_los_cds)
        rutas_por_cd[cd_mas_cercano].append(indice_tienda)
        
    # formatear la solucion final: [CD, tienda1, tienda2, ..., CD]
    solucion_formateada = []
    for i, tiendas_para_un_cd in enumerate(rutas_por_cd):
        # cada ruta inicia y termina en el CD
        una_ruta = [i] + tiendas_para_un_cd + [i]
        solucion_formateada.append(una_ruta)
        
    return solucion_formateada

def generar_solucion_vecina(solucion_actual: TipoSolucion, matriz_de_distancias: np.ndarray) -> TipoSolucion:
    # generar una solucion vecina haciendo un swap de dos tiendas en una ruta aleatoria

    nueva_solucion_vecina = [list(ruta) for ruta in solucion_actual] # copia de la solucion actual
    
    # seleccionar una ruta aleatoria
    indice_de_ruta_aleatoria = random.randint(0, NUMERO_DE_CDS - 1) 
    ruta_seleccionada = nueva_solucion_vecina[indice_de_ruta_aleatoria]
    
    # Una ruta debe tener al menos 2 tiendas para poder intercambiar y minimo 4 nodos: CD, T1, T2, CD
    if len(ruta_seleccionada) < 4:
        return nueva_solucion_vecina # devuelve la misma solucion si no hay tiendas para mover
        
    # seleccionar dos indices de tienda para intercambiar
    # excluimos el CD inicial y el final 
    indices_para_intercambiar = random.sample(range(1, len(ruta_seleccionada) - 1), 2)
    indice1, indice2 = indices_para_intercambiar[0], indices_para_intercambiar[1]
    
    # realizar el intercambio 
    ruta_seleccionada[indice1], ruta_seleccionada[indice2] = ruta_seleccionada[indice2], ruta_seleccionada[indice1]
    # retornar la nueva solucion vecina
    return nueva_solucion_vecina