import pytest
import allure
import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.public_page import PublicPage

@pytest.fixture
def df():
    # Leer el archivo CSV en un DataFrame
    csv_path = './data/PRES_2024.csv'
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

@pytest.fixture
def screenshots_folder():
    # Define la ruta de la carpeta donde almacenarás las capturas de pantalla
    return "screenshots_publi"

@pytest.mark.parametrize("allure_story, valor, tipo_dato, selector, ruta", PublicPage.leer_datos_csv('/var/jenkins_home/workspace/Publicacion_POM/data/elementos.csv'))
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

    #valor_csv = "{:,.0f}".format(int(df[valor].iloc[0]))
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

        #file_path = PublicPage.get_next_screenshot_path('captura_elemento')
        #BasePage.capture_element_screenshot(elemento, file_path)
        #print(f"Captura de pantalla guardada en: {file_path}")
        file_path = public_page.highlight_and_capture_element(elemento, 'screenshots_publi')
        
        with allure.step("Comparando los valores de sitio vs csv"):
            if valor_en_pagina == valor_csv:
                allure.attach(
                    f"Los valores coinciden, Sitio: {valor_en_pagina} CSV: {valor_csv}",
                    name="Resultado de la validación",
                    attachment_type=allure.attachment_type.TEXT
                )
                with open(file_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="Captura de pantalla del elemento",
                        attachment_type=allure.attachment_type.PNG
                    )
            else:
                allure.attach(
                    f"Los valores no coinciden, Sitio: {valor_en_pagina} CSV: {valor_csv}",
                    name="Resultado de la validación",
                    attachment_type=allure.attachment_type.TEXT
                )
                with open(file_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="Captura de pantalla del error",
                        attachment_type=allure.attachment_type.PNG
                    )
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