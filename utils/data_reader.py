import pandas as pd
import os

class data_reader():
    # Función para leer datos desde el CSV y eliminar el BOM si está presente
    @staticmethod
    def leer_datos_csv():
        filepath = '/var/jenkins_home/workspace/Publicacion_POM/data/elementos.csv'
        df = pd.read_csv(filepath, encoding='utf-8-sig')

        for index, row in df.iterrows():
            yield row['allure_story'], row['valor'], row['tipo_dato'], row['selector'], row['ruta']

    @staticmethod
    def df():
        # Leer el archivo CSV en un DataFrame
        csv_path = '/var/jenkins_home/workspace/Publicacion_POM/tests/data/PRES_2024.csv'
        df = pd.read_csv(csv_path, skiprows=3, nrows=1, header=None, names=[
            "ACTAS_ESPERADAS", "ACTAS_REGISTRADAS", "ACTAS_FUERA_CATALOGO", 
            "ACTAS_CAPTURADAS", "PORCENTAJE_ACTAS_CAPTURADAS", 
            "ACTAS_CONTABILIZADAS", "PORCENTAJE_ACTAS_CONTABILIZADAS", 
            "PORCENTAJE_ACTAS_INCONSISTENCIAS", "ACTAS_NO_CONTABILIZADAS", 
            "LISTA_NOMINAL_ACTAS_CONTABILIZADAS", "TOTAL_VOTOS_C_CS", 
            "TOTAL_VOTOS_S_CS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
        ])

        # Retornar solo las columnas necesarias en un nuevo DataFrame
        selected_columns = df[[
            "ACTAS_ESPERADAS", "ACTAS_CAPTURADAS", "ACTAS_CONTABILIZADAS", "LISTA_NOMINAL_ACTAS_CONTABILIZADAS", "TOTAL_VOTOS_C_CS", "TOTAL_VOTOS_S_CS", "PORCENTAJE_ACTAS_CAPTURADAS", "PORCENTAJE_PARTICIPACION_CIUDADANA"
        ]]

        return selected_columns