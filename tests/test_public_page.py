import pytest
import allure
import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.data_reader import data_reader
from pages.public_page import PublicPage
from utils.utils import Utils

@pytest.fixture
def df():
    return data_reader.df()

@pytest.fixture
def screenshots_folder():
    return "screenshots_publi"

@pytest.mark.parametrize("allure_story, valor, tipo_dato, selector, ruta", data_reader.leer_datos_csv())
@allure.feature('Validación de datos en sitio de Publicación - POM')
def test_validacion_datos(setup, df, allure_story, valor, tipo_dato, selector, ruta, screenshots_folder):
    """
    Prueba que los valores del encabezado del CSV coincidan con el sitio de publicacion: 
    https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura
    """
    # Aplicar la etiqueta @allure.story dinámicamente
    allure.dynamic.story(allure_story)  # Etiqueta dinámica basada en el CSV

    # Establecer un título dinámico para la prueba
    allure.dynamic.title(allure_story)

    # Validar el formato según el tipo de dato
    if tipo_dato == 'int':
        valor_csv = "{:,.0f}".format(int(df[valor].iloc[0]))
    elif tipo_dato == 'float':
        valor_csv = "{:,.4f}".format(float(df[valor].iloc[0]))
    else:
        pytest.fail(f"Tipo de dato no reconocido: {tipo_dato}")

    # Convertir el tipo de localizador a su objeto correspondiente de Selenium
    locator_type_obj = eval(selector)
    
    try:
        driver = setup
        public_page = PublicPage(driver)
        elemento = driver.find_element(locator_type_obj, ruta)
        if tipo_dato == 'int':
            valor_en_pagina = elemento.text
        elif tipo_dato == 'float':
            valor_en_pagina2 = elemento.text
            valor_en_pagina = re.sub(r'[^\d.]', '', valor_en_pagina2)
        else:
            pytest.fail(f"Tipo de dato no reconocido: {tipo_dato}")

        file_path = public_page.highlight_and_capture_element(elemento, 'screenshots_publi')
        
        Utils.attach_allure_results(valor_en_pagina, valor_csv, file_path)

        # Manejo de excepciones para múltiples validaciones
        resultados_fallidos = []
        try:
            assert valor_en_pagina == valor_csv
        except AssertionError as e:
            resultados_fallidos.append(f"Falló en: {allure_story} - Sitio: {valor_en_pagina} CSV: {valor_csv}")

        if resultados_fallidos:
            pytest.fail(f"Error en validación: {', '.join(resultados_fallidos)}")
            
    except NoSuchElementException:
        # Manejar la excepción si el elemento no se encuentra
        error_message = f"Elemento no encontrado: {selector} - {ruta}"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(error_message)