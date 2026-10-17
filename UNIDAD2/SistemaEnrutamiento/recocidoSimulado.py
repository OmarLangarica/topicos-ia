import math
import random
from typing import List, Tuple
import numpy as np

from funcionDeCosto import calcular_costo_total_de_solucion, TipoSolucion
from solucion import crear_solucion_inicial, generar_solucion_vecina

def ejecutar_recocido_simulado(
    matriz_de_distancias: np.ndarray,
    matriz_de_costos: np.ndarray,
    temp_inicial: float,              # Temperatura inicial
    temp_final: float,                # Temperatura final
    factor_enfriamiento: float,       # Factor de enfriamiento
    iteraciones_por_temp: int         # Iteraciones por temperatura
) -> Tuple[TipoSolucion, float, List[float]]:
    
    # inicializacion de la solucion y calculo de su costo
    solucion_actual = crear_solucion_inicial(matriz_de_distancias)
    costo_actual = calcular_costo_total_de_solucion(solucion_actual, matriz_de_distancias, matriz_de_costos)
    
    # guardar la mejor solucion encontrada y su costo
    mejor_solucion = [list(ruta) for ruta in solucion_actual]
    mejor_costo = costo_actual 
    
    temperatura_actual = temp_inicial  # temperatura actual
    historial_de_costos = [costo_actual]
    contador_ciclos_temperatura = 0 # contador para los ciclos de enfriamiento
    
    # impresion inicial
    print("Temperatura inicial: " + str(temp_inicial) + ", Factor de enfriamiento: " + str(factor_enfriamiento))
    print("Costo de la solución inicial: $" + str.format('{:,.2f}', costo_actual) + " MXN")
    
    print("\n| Ciclo | Temperatura | Costo Actual | Mejor Costo |")
    print("|-------|-------------|--------------|-------------|")
    print("| " + str(contador_ciclos_temperatura).center(5) + " | " + str.format('{:11.4f}', temperatura_actual) + " | $" + str.format('{:^8.2f}', costo_actual) + "    | $" + str.format('{:^7.2f}', mejor_costo) + "    |")
    
    # bucle principal del recocido como criterio de parada la temperatura final 
    while temperatura_actual > temp_final:
        contador_ciclos_temperatura += 1
        
        for _ in range(iteraciones_por_temp):  # realiza L iteraciones a esta temperatura
            
            #generamos vecino y evaluamos su costo
            nueva_solucion = generar_solucion_vecina(solucion_actual, matriz_de_distancias)
            nuevo_costo = calcular_costo_total_de_solucion(nueva_solucion, matriz_de_distancias, matriz_de_costos)
            
            # diferencia de costo entre la nueva solucion y la actual
            diferencia_de_costo = nuevo_costo - costo_actual
            
            # criterio de aceptacion
            if diferencia_de_costo < 0:
                solucion_actual = nueva_solucion
                costo_actual = nuevo_costo
            else:
                # se acepta con probabilidad de aceptacion si es peor
                probabilidad_de_aceptacion = math.exp(-diferencia_de_costo / temperatura_actual)
                if random.random() < probabilidad_de_aceptacion:
                    solucion_actual = nueva_solucion
                    costo_actual = nuevo_costo
            
            # actualiza la mejor solucion global
            if costo_actual < mejor_costo:
                mejor_solucion = [list(ruta) for ruta in solucion_actual]
                mejor_costo = costo_actual
            
            historial_de_costos.append(costo_actual)
        
        # enfriamiento geometrico
        temperatura_actual *= factor_enfriamiento
    
        print("| " + str(contador_ciclos_temperatura).center(5) + " | " + str.format('{:11.4f}', temperatura_actual) + " | $" + str.format('{:^8.2f}', costo_actual) + " | $" + str.format('{:^7.2f}', mejor_costo) + " |")
    # retornamos la mejor solucion encontrada y su costo
    return mejor_solucion, mejor_costo, historial_de_costos