# error: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently
# https://stackoverflow.com/questions/76187256/importerror-urllib3-v2-0-only-supports-openssl-1-1-1-currently-the-ssl-modu/78621375#78621375

# La razón por la cual el mensaje de error menciona OpenSSL 1.1.1+ y LibreSSL 2.8.3 es que urllib3 v2.0 
# (la versión que ha instalado) requiere OpenSSL 1.1.1+ para funcionar correctamente, ya que depende de 
# algunas características nuevas de OpenSSL. 1.1.1.El problema es que la versión del módulo 'ssl' que 
# está instalado actualmente en su entorno está compilada con LibreSSL 2.8.3, que no es compatible con urllib3 v2.0.
# Para usar urllib3 v2.0, necesita un módulo 'ssl' compilado con OpenSSL 1.1.1 o posterior, intentando:  

# pip install urllib3==1.26.6

# from seleniumwire import webdriver  # Import from seleniumwire
from selenium import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import aspose.imaging as imaging

import urllib.request
import urllib.parse
from urllib.parse import urlparse, parse_qs

# import seleniumwire.webdriver as webdriver  # Import from seleniumwire

def base_code_01():
    options = Options()
    options.add_argument("--headless")

    # Create a new instance of the Chrome driver
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 60)

    # Go to the Google home page
    driver.get('https://hasbercourier.easyenvios.com/')

    sum = '1337566'

    # //*[@id="txtseguimiento"]
    input_element = wait.until(EC.presence_of_element_located((By.ID, 'txtseguimiento')))

    # Send keys to the input field
    input_element.send_keys(sum)

    button_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/section/div/div/div[1]/div/form/div[2]/button')))

    # Assuming you want the first button in the list
    if button_elements:
        button_elements[0].click()  # Click the first button in the list
    
        time.sleep(3)

        parsear_frame = wait.until(EC.presence_of_element_located((By.ID, 'ifrmvisorcargo')))
        src = parsear_frame.get_attribute('src')
        parsed_url = urlparse(src)

        # Parsear los parámetros de la query string
        query_params = parse_qs(parsed_url.query)

        # Obtener el valor del parámetro 'url'
        file_url = query_params.get('url', [None])[0]

        post_data = file_url

        # encoded_data = urllib.parse.urlencode(post_data).encode('utf-8')

        # Especificar el nombre y ruta del archivo que deseas guardar
        file_name = sum+'.tif'

        # Realizar la solicitud POST y descargar el archivo
        try:
            with urllib.request.urlopen(urllib.request.Request(post_data)) as response, open(file_name, "wb") as out_file:
                data = response.read()
                out_file.write(data)

            print(f"Archivo guardado como {file_name}")

            import aspose.words as aw

            # Cargar el archivo TIFF
            doc = aw.Document()
            builder = aw.DocumentBuilder(doc)
            builder.insert_image(f"{sum}.tif")

            # Guardar como PDF
            doc.save(f"{sum}.pdf")
            
            print(f'Archivo TIFF convertido a PDF y guardado en {sum}.pdf')

        except Exception as e:
            print(f"Error al descargar el archivo: {e}")

    else:
        print("No buttons found")

import time
import Constant as C
from queue import Queue

def base_code_02():
    # Decorador para medir el tiempo de ejecución
    def medir_tiempo(func):
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            print(f"{func.__name__} tomó {fin - inicio:.2f} segundos")
            return resultado
        return wrapper

    def test_queue(driver,wait,s):
        # Crear una queue (cola)
        cola = Queue()

        # Encolar (agregar) elementos a la cola
        cola.put(s)

        # Obtener y mostrar los elementos de la cola
        print("Elementos de la cola:")

        while not cola.empty():
            # Desencolar y mostrar el elemento
            elemento = cola.get()
            driver.execute_script("window.open('https://hasbercourier.easyenvios.com/', 'twotab');")
            driver.switch_to.window(driver.window_handles[-1])
            suburl = test_add(wait,elemento)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(suburl)
            # driver.switch_to.window(window_handles[0])
            # time.sleep(2)
            # print('over')
            # print(elemento)

    @medir_tiempo
    def test_add(wait,suministro):
        time.sleep(2)
        sandbox = wait.until(EC.presence_of_element_located((By.ID, C.exp.box)))
        sandbox.send_keys(suministro)

        sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.btn)))
        sendContent[0].click()

        time.sleep(3)
        Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
        return Framesubdoc

    def test_navigator():
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        wait = WebDriverWait(driver, 60)
        driver.get('https://hasbercourier.easyenvios.com/')
        return driver,wait

    www = [1337534,1337535,1337536,1337534,1337535,1337536]
    driver,wait = test_navigator()
    test_queue(driver,wait,www[0])
    test_queue(driver,wait,www[1])


# base_code_02()

# def test_src_subdoc(wait,suministro):
#     time.sleep(2)
#     sandbox = wait.until(EC.presence_of_element_located((By.ID, C.exp.box)))
#     sandbox.send_keys(suministro)

#     sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.btn)))
#     sendContent[0].click()

#     time.sleep(3)
#     Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
#     return Framesubdoc

# def test_queue_(driver,wait,suministro):

#     driver.execute_script("window.open('https://hasbercourier.easyenvios.com/', '');")

#     # Crear una queue (cola)
#     cola = Queue()

#     # Encolar (agregar) elementos a la cola
#     cola.put(suministro)

#     # Obtener y mostrar los elementos de la cola
#     print("Elementos de la cola:",cola.get())

#     test_src_subdoc(wait,cola.get())
    
# def base_code_03():
#     options = Options()
#     # options.add_argument("--headless")
#     driver = webdriver.Firefox(options=options)
#     wait = WebDriverWait(driver, 60)
#     driver.get('https://hasbercourier.easyenvios.com/')
#     return driver,wait

#     # sandbox = wait.until(EC.presence_of_element_located((By.ID,C.exp.box)))
#     # sandbox.send_keys(suministro)

#     # sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH,C.exp.btn)))
#     # sendContent[0].click()

#     # time.sleep(3)
#     # Framesubdoc = wait.until(EC.presence_of_element_located((By.ID,C.exp.subdoc))).get_attribute('src')
#     # driver.quit()

#     # return Framesubdoc, suministro

# # las peticiones nunca seran al mismo tiempo
# dd = [1337534,1337535,1337536,1337534,1337535,1337536]
# driver,wait = base_code_03()
# test_queue_(driver,wait,dd[0])
# # time.sleep(6)
# # test_queue_(driver,wait,dd[1])
# # for s in www:
# #     test_queue_(driver,wait,s)
