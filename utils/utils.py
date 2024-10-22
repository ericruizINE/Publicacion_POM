from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class Utils:
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

    def attach_allure_results(valor_en_pagina, valor_csv, file_path):
        """
        Adjunta resultados a Allure dependiendo de si los valores coinciden o no.
        """
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
