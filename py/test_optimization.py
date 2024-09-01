import time
from queue import Queue
import Constant as C
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import WebDriverException

import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Variables globales para el WebDriver y WebDriverWait
driver = None
wait = None

def medir_tiempo(func):
    """
    Decorador para medir el tiempo de ejecución de una función.
    
    Args:
        func: La función a decorar.
    
    Returns:
        wrapper: Función decorada que mide el tiempo de ejecución.
    """
    def wrapper(*args, **kwargs):
        inicio = time.time()
        try:
            resultado = func(*args, **kwargs)
        except Exception as e:
            print(f"Error en {func.__name__}: {e}")
            raise
        fin = time.time()
        print(f"{func.__name__} tomó {fin - inicio:.2f} segundos")
        return resultado
    return wrapper

def cargo_de_envios(wait):
    time.sleep(3)
    table_send = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.table)))
    for n_ in range(len(table_send)):
        table_tr = wait.until(EC.presence_of_element_located((By.XPATH,C.exp.tr.replace('@',f'{n_+1}')))).click()
        # time.sleep(2)
        info = wait.until(EC.presence_of_element_located((By.ID,'sp_cargo_documento'))).text
        if 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS' == info:
            # time.sleep(1)
            Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
            return Framesubdoc
        
        elif 'VOLANTES / AVISO DE CORTE' == info:
            return 'No hay carta de CAMBIO DE MEDIDOR solo AVISO DE CORTE'
    
@medir_tiempo
def test_add(wait, suministro):
    """
    Interactúa con una página web para enviar un suministro y obtener un atributo del iframe.
    
    Args:
        wait: Objeto WebDriverWait para manejar las esperas explícitas.
        suministro: El valor a enviar en el formulario.
    
    Returns:
        str: El valor del atributo 'src' del iframe.
    """
    try:
        time.sleep(2)
        sandbox = wait.until(EC.presence_of_element_located((By.ID, C.exp.box)))
        sandbox.send_keys(suministro)

        sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.btn)))
        sendContent[0].click()

        rs = cargo_de_envios(wait)
        return rs
    
        # time.sleep(3)
        # Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
        # return Framesubdoc

    except Exception as e:
        print(f"Error en test_add: {e}")
        return None

def test_queue(driver, wait, suministro):
    """
    Maneja la cola de suministros, abre nuevas pestañas, y llama a test_add para un suministro.
    
    Args:
        driver: Instancia del WebDriver.
        wait: Objeto WebDriverWait para manejar las esperas explícitas.
        suministro: Valor del suministro para procesar.
    
    Returns:
        str: Resultado del procesamiento del suministro.
    """
    cola = Queue()
    cola.put(suministro)
    result = None

    while not cola.empty():
        elemento = cola.get()
        try:
            driver.execute_script("window.open('https://hasbercourier.easyenvios.com/', '');")
            driver.switch_to.window(driver.window_handles[-1])
            result = test_add(wait, elemento)
        except Exception as e:
            print(f"Error al procesar elemento {elemento}: {e}")
            result = None
        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    
    return result

def init_browser():
    """
    Inicializa el WebDriver y abre la página principal al iniciar la aplicación.
    """
    global driver, wait
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 60)
    try:
        driver.get('https://hasbercourier.easyenvios.com/')        
    except Exception as e:
        print(f"Error al abrir la página principal: {e}")
        driver.quit()
        raise

@app.route('/procesar_suministro', methods=['POST'])
def procesar_suministro():
    """
    Endpoint para procesar un suministro.
    
    Expects:
        JSON body with a single suministro.
    
    Returns:
        JSON response with the result of processing the suministro.
    """
    data = request.json
    suministro = data.get('suministro')
    
    if suministro is None:
        return jsonify({"error": "Debe proporcionar un suministro."}), 400
    try:
        result = test_queue(driver, wait, suministro)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

if __name__ == "__main__":
    init_browser()  # Inicializa el navegador cuando se inicia la aplicación
    app.run(host='0.0.0.0',port=5000)