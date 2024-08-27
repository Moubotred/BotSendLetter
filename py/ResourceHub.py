from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import json
import shutil
import urllib.parse
import urllib.request
import py.Constant as C
import aspose.words as aw
from getpass import getuser
import aspose.imaging as imaging
from urllib.parse import urlparse, parse_qs

def SearchFileWeb(suministro):
    """
    Realiza una búsqueda en la página web especificada utilizando el suministro proporcionado.
    
    Abre un navegador Firefox en modo sin cabeza (headless) para acceder a la página web,
    ingresa el suministro en un campo de texto y realiza una acción para obtener un documento relacionado.
    
    Args:
        suministro (str): El suministro que se utilizará para buscar el archivo en la web.
    
    Returns:
        tuple: Una tupla que contiene la URL del documento incrustado en la página web (Framesubdoc) y el suministro utilizado.
    """
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 60)
    driver.get('https://hasbercourier.easyenvios.com/')

    sandbox = wait.until(EC.presence_of_element_located((By.ID, C.exp.box)))
    sandbox.send_keys(suministro)

    sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.btn)))
    sendContent[0].click()

    time.sleep(3)
    Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
    driver.quit()

    return Framesubdoc, suministro

def UrlSubdoc(Framesubdoc):
    """
    Extrae la URL del documento de un iframe embebido en la página web.
    A partir de la URL del iframe, parsea los parámetros de la URL y 
    extrae el valor del parámetro 'url'.

    Args:
        Framesubdoc (str): La URL del iframe que contiene el documento.

    Returns:
        str: La URL directa del documento o None si no se encuentra el parámetro 'url'.
    """
    ParsedUrl = urlparse(Framesubdoc)
    QueryParams = parse_qs(ParsedUrl.query)
    Url = QueryParams.get('url', [None])[0]
    return Url

def FileWebDownloads(url, suministro):
    """
    Descarga un archivo desde la URL especificada y lo guarda en el 
    sistema de archivos con un nombre basado en el suministro.

    Si la descarga es exitosa, el archivo se guarda con el nombre '<suministro>.tif'. 
    En caso de error, se captura la excepción y se imprime un mensaje.

    Args:
        url (str): La URL desde la que se descargará el archivo.
        suministro (str): El suministro que se utilizará para nombrar el archivo descargado.

    Returns:
        str: El nombre del archivo descargado o None si ocurrió un error durante la descarga.
    """
    try:
        if url != 'http://www.easyenvios.com/escan1/006/003/3/00000001/01/00300000001000001.TIF':
            filename = suministro + '.tif'
            with urllib.request.urlopen(urllib.request.Request(url)) as response, open(filename, "wb") as out_file:
                data = response.read()
                out_file.write(data)
            return filename  # Es importante retornar el nombre del archivo aquí
        else:
            return False

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None

def ConvertPdf(filename):
    """
    Convierte un archivo TIFF a PDF utilizando la biblioteca Aspose.Words.

    Si el archivo TIFF se ha descargado correctamente, se inserta en un nuevo documento PDF
    y se guarda con el mismo nombre pero con extensión '.pdf'. Si el archivo no se descargó correctamente,
    se imprime un mensaje de error.

    Args:
        filename (str): El nombre del archivo TIFF que se convertirá a PDF.
    """

    if filename:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.insert_image(filename)
        doc.save(filename.replace('.tif', '.pdf'))
        return filename.replace('.tif', '.pdf')
        # print(f"Archivo TIFF convertido a PDF y guardado en {filename.replace('.tif', '.pdf')}")
    else:
        return False
        # print("No se pudo convertir a PDF porque el archivo TIFF no se descargó correctamente.")

def Templades(resp):
        if resp != False:
            path = r'C:\Users\{}\Documents\Js\Bot\py\pdf'.format(getuser())
            os.makedirs(path,exist_ok=True)

            # direct = []
            # for _ in range(2):
            #     path = os.path.dirname(path)
            #     direct.append(path)

            # os.chdir(direct[1])
            
            files = os.listdir()

            pdf_destination = r'C:\Users\{}\Documents\Js\Bot\py\pdf'.format(getuser())
            os.makedirs(pdf_destination, exist_ok=True)

            # Filtrar y procesar archivos
            for file in files:
                if file.endswith('.tif'):
                    # Eliminar archivos .tif
                    os.remove(file)
                    # print(f'Archivo eliminado: {file}')
                elif file.endswith('.pdf'):
                    # Mover archivos .pdf al destino
                    shutil.move(file, os.path.join(pdf_destination, file))
                    # print(f'Archivo movido: {file} -> {pdf_destination}')
        else:
            pass

def ConsultApi(ip,port,endpoint,key_data,suministro):
    
    # url = "http://localhost:4000/procesar_suministro"
    # url = "http://localhost:5000/search"
    
    url = f"http://{ip}:{port}/{endpoint}"

    # Crear los datos en formato JSON
    data = {
        "suministro": suministro  # Reemplaza con el suministro que quieras enviar
    }

    # Convertir los datos a un formato de bytes
    data_bytes = json.dumps(data).encode('utf-8')

    # Configurar la solicitud POST
    req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'}, method='POST')

    # Hacer la solicitud y leer la respuesta
    try:
        with urllib.request.urlopen(req) as response:
            # Leer la respuesta y decodificarla
            response_data = response.read().decode('utf-8')
            # Convertir la respuesta a un diccionario
            result = json.loads(response_data)
            data = result.get(key_data)
            return data

    except urllib.error.HTTPError as e:
        print(f'Error HTTP: {e.code} - {e.reason}')
    except urllib.error.URLError as e:
        print(f'Error URL: {e.reason}')