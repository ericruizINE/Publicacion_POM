from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by_locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by_locator))

    def click(self, by_locator):
        self.wait_for_element(by_locator)
        self.driver.find_element(*by_locator).click()

    def enter_text(self, by_locator, text):
        self.wait_for_element(by_locator)
        self.driver.find_element(*by_locator).send_keys(text)

    def get_text(self, by_locator):
        self.wait_for_element(by_locator)
        return self.driver.find_element(*by_locator).text

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