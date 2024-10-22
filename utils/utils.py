from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from pages.base_page import BasePage
class Utils(BasePage):
    def capture_element_screenshot(self, element, file_path):
        """
        Captura una captura de pantalla resaltando el elemento específico con un borde.
        """
        # Obtener el tamaño total de la página
        total_width = self.driver.execute_script("return document.body.scrollWidth")
        total_height = self.driver.execute_script("return document.body.scrollHeight")

        # Establecer el tamaño de la ventana al tamaño total de la página
        self.driver.set_window_size(total_width, total_height)
        # Resaltar el elemento usando JavaScript
        self.driver.execute_script("arguments[0].style.border='9px solid red'", element)
        
        # Desplazar la página hasta que el elemento esté visible
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        # Esperar a que el elemento sea visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(element)
        )

        # Capturar la pantalla completa
        self.driver.save_screenshot(file_path)

        #allure.attach(self.driver.get_screenshot_as_png(), name="Element Screenshot", attachment_type=AttachmentType.PNG)

        # Quitar el borde después de la captura
        self.driver.execute_script("arguments[0].style.border=''", element)

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
