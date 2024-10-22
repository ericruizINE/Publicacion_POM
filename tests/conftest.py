import pytest
import chromedriver_autoinstaller
from selenium import webdriver
import os  
import pytest  
from pytest_metadata.plugin import metadata_key  

@pytest.fixture(scope="function")
def setup():
    # Configurar el controlador de Chrome
    print(f"Current working directory: {os.getcwd()}")
    chromedriver_autoinstaller.install() 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("Versión chromedriver:", driver.capabilities['browserVersion'])
    driver.maximize_window()

    # URL de la página que deseas validar
    url = 'https://prep2024.ine.mx/publicacion/nacional/presidencia/nacional/candidatura'
    driver.get(url)

    # Espera a que la página cargue completamente
    driver.implicitly_wait(10)
    
    yield driver  # Retorna el driver para usarlo en las pruebas
    
    driver.quit()  # Asegúrate de cerrar el navegador después de la prueba

def pytest_html_report_title(report):  
    report.title = "Reporte Pruebas de Publicación"  
  
def pytest_configure(config):  
    config.stash[metadata_key]["Project"] = "Pruebas Sitio Publicación y CSV"  