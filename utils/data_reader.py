import pandas as pd
import os

def leer_datos_csv():
    """
    Lee el archivo CSV y elimina el BOM si está presente. Genera las filas necesarias
    para la parametrización de pytest en la prueba.
    """
    csv_path = os.path.join(os.path.abspath(__file__), 'data', 'elementos.csv')
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    data = []

    for index, row in df.iterrows():
        data.append((row['allure_story'], row['valor'], row['selector'], row['ruta']))

    return data
