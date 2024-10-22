import os
import pytest
from selenium.webdriver.common.by import By
import pandas as pd
from .base_page import BasePage

class PublicPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.screenshots_folder = 'screenshots_publi'
        self.ensure_screenshot_folder()

    def ensure_screenshot_folder(self):
        if not os.path.exists(self.screenshots_folder):
            os.makedirs(self.screenshots_folder)

    def get_next_screenshot_path(self, screenshots_folder, base_filename):
        """Genera el siguiente nombre de archivo disponible con un número consecutivo."""
        i = 1
        while True:
            filename = f"{base_filename}_{i:03d}.png"
            path = os.path.join(screenshots_folder, filename)
            if not os.path.exists(path):
                return path
            i += 1

    def highlight_and_capture_element(self, elemento, screenshots_folder):
        """Resalta y captura un elemento específico de la página pública."""
        element = elemento
        file_path = self.get_next_screenshot_path(screenshots_folder, 'captura_elemento')
        self.capture_element_screenshot(element, file_path)
        print(f"Captura de pantalla guardada en: {file_path}")
        return file_path  # Retorna la ruta de la captura de pantalla
        

    # Función para leer datos desde el CSV y eliminar el BOM si está presente
    def leer_datos_csv(filepath):
        df = pd.read_csv(filepath, encoding='utf-8-sig')

        for index, row in df.iterrows():
            yield row['allure_story'], row['valor'], row['tipo_dato'], row['selector'], row['ruta']
    
    def df():
        # Leer el archivo CSV en un DataFrame
        csv_path = '/var/jenkins_home/workspace/Publicacion_POM/data/PRES_2024.csv'
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