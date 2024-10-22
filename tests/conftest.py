import pytest
import chromedriver_autoinstaller
from selenium import webdriver
import os  
import pytest  
import requests
import zipfile
from pytest_metadata.plugin import metadata_key  

@pytest.fixture(scope="function")
def setup():
    # Configurar el controlador de Chrome
    #chromedriver_autoinstaller.install() 
    try:
        chromedriver_autoinstaller.install()
    except Exception as e:
        print(f"Error descargando ChromeDriver: {e}")
        # Agrega código aquí para manejar la excepción, como descargar manualmente
        descargar_chromedriver_manual(version="128.0.6613.86")
        driver_path = "./driver/chromedriver/chromedriver"  # Asegúrate de que sea la ruta correcta
        driver = webdriver.Chrome(executable_path=driver_path)

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

def descargar_chromedriver_manual(version="128.0.6613.86"):
    # URL para la descarga del chromedriver desde la página oficial (ajustar la versión si es necesario)
    url = f"https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/linux64/chromedriver-linux64.zip"
    archivo_zip = "chromedriver_linux64.zip"
    directorio_descarga = "./driver/chromedriver/"  # Cambiar a la ruta deseada dentro del venv

    # Crear el directorio si no existe
    if not os.path.exists(directorio_descarga):
        os.makedirs(directorio_descarga)

    # Descargar el archivo
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(directorio_descarga, archivo_zip), 'wb') as file:
            file.write(response.content)
        print(f"ChromeDriver {version} descargado exitosamente.")
        
        # Extraer el archivo ZIP
        with zipfile.ZipFile(os.path.join(directorio_descarga, archivo_zip), 'r') as zip_ref:
            zip_ref.extractall(directorio_descarga)
        print(f"ChromeDriver extraído en {directorio_descarga}.")
        
        # Opcionalmente, puedes establecer permisos de ejecución si estás en Linux
        os.chmod(os.path.join(directorio_descarga, "chromedriver"), 0o755)
    else:
        print(f"No se pudo descargar ChromeDriver. Código de estado: {response.status_code}")
