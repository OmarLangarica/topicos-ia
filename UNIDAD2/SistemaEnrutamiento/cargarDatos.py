import pandas as pd
import numpy as np
from pathlib import Path


def _leer_tabla(ruta_archivo: str) -> pd.DataFrame:
    """Lee archivos CSV o Excel manteniendo una única ruta de carga."""
    extension = Path(ruta_archivo).suffix.lower()
    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(ruta_archivo)
    if extension == ".csv":
        return pd.read_csv(ruta_archivo, encoding="latin1")
    raise ValueError(
        f"Formato no soportado para '{ruta_archivo}'. "
        "Usa un archivo .xlsx, .xls o .csv."
    )


def cargar_datos_desde_archivos(
    archivo_coordenadas: str, 
    archivo_distancias: str, 
    archivo_costos: str
    ) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]: # (coordenadas, distancia, costo)
    try:
        coordenadas = _leer_tabla(archivo_coordenadas)
        matriz_de_distancias = _leer_tabla(archivo_distancias).to_numpy(dtype=float)
        costos_combustible = _leer_tabla(archivo_costos).to_numpy(dtype=float)

        columnas_requeridas = {
            "Tipo",
            "Nombre",
            "Latitud_WGS84",
            "Longitud_WGS84",
        }
        columnas_faltantes = columnas_requeridas.difference(coordenadas.columns)
        if columnas_faltantes:
            raise ValueError(
                "Faltan columnas en el archivo de coordenadas: "
                + ", ".join(sorted(columnas_faltantes))
            )

        numero_de_nodos = len(coordenadas)
        forma_esperada = (numero_de_nodos, numero_de_nodos)
        if matriz_de_distancias.shape != forma_esperada:
            raise ValueError(
                f"La matriz de distancias tiene forma {matriz_de_distancias.shape}; "
                f"se esperaba {forma_esperada}."
            )
        if costos_combustible.shape != forma_esperada:
            raise ValueError(
                f"La matriz de costos tiene forma {costos_combustible.shape}; "
                f"se esperaba {forma_esperada}."
            )

        coordenadas = coordenadas.reset_index(drop=True)
        return coordenadas, matriz_de_distancias, costos_combustible

    except FileNotFoundError as fnfe:
        print("Error: verifica que los archivos estén en la carpeta Datos: " + str(fnfe))
        raise
    except Exception as e:
        print("Error al cargar los datos: " + str(e))
        raise