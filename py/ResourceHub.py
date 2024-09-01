import os
import json
import time
import shutil
import urllib.parse
import urllib.request
from getpass import getuser
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import aspose.words as aw
import aspose.imaging as imaging
import py.Constant as C

request_logs = []

def cache(suministro):
    path = r'C:\Users\{}\Documents\Js\Bot\py\pdf'.format(getuser())
    os.makedirs(path, exist_ok=True)
    
    pdf_filename = f"{suministro}.pdf"
    if pdf_filename in os.listdir(path):
        return os.path.join(path, pdf_filename)
    else:
        return None

# def load_existing_logs(filename):
#     try:
#         with open(filename, 'r') as file:
#             if file.read(1):
#                 file.seek(0)  # Rewind the file if not empty
#                 return json.load(file)
#             else:
#                 return {}  # Return an empty dict if file is empty
#     except FileNotFoundError:
#         return {}  # Return an empty dict if file does not exist
#     except json.JSONDecodeError:
#         return {}  # Return an empty dict if JSON is invali
    
# def save_logs_to_file(logs, filename='request_logs.json'):
#     """
#     Guarda los registros en el archivo JSON, reemplazando el contenido existente.
#     """
#     with open(filename, 'w') as file:
#         json.dump(logs, file, indent=4)

# def log_request(suministro, response_data, filename='request_logs.json'):
#     """
#     Registra la solicitud y la respuesta en un formato JSON.
#     """
#     try:
#         # Cargar registros existentes
#         logs = load_existing_logs(filename)
        
#         # Agregar el nuevo registro
#         request_log = {
#             "suministro": suministro,
#             "response": response_data
#         }
#         logs.append(request_log)
        
#         # Guardar los registros actualizados en el archivo JSON
#         save_logs_to_file(logs, filename)

#     except AttributeError:
#         pass

# def obtener_valores(suministro,datos):
#     for item in datos:
#         if item['suministro'] == suministro:
#             return item['response']
#     return None


def SearchFileWeb(suministro):
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 60)
    driver.get('https://hasbercourier.easyenvios.com/')

    sandbox = wait.until(EC.presence_of_element_located((By.ID, C.exp.box)))
    sandbox.send_keys(suministro)

    sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.btn)))
    sendContent[0].click()

    time.sleep(2)

    table_send = wait.until(EC.presence_of_all_elements_located((By.XPATH, C.exp.table)))
    for n_ in range(len(table_send)):
        table_tr = wait.until(EC.presence_of_element_located((By.XPATH,C.exp.tr.replace('@',f'{n_+1}')))).click()
        info = wait.until(EC.presence_of_element_located((By.ID,'sp_cargo_documento'))).text
        if 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS' == info:
            time.sleep(2)
            Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, C.exp.subdoc))).get_attribute('src')
            driver.quit()
            print(Framesubdoc)
            return Framesubdoc, suministro
        else:
            pass

def UrlSubdoc(Framesubdoc):
    ParsedUrl = urlparse(Framesubdoc)
    QueryParams = parse_qs(ParsedUrl.query)
    Url = QueryParams.get('url', [None])[0]
    return Url

def FileWebDownloads(url, suministro):
    try:
        if url != 'http://www.easyenvios.com/escan1/006/003/3/00000001/01/00300000001000001.TIF':
            filename = suministro + '.tif'
            with urllib.request.urlopen(urllib.request.Request(url)) as response, open(filename, "wb") as out_file:
                data = response.read()
                out_file.write(data)
            return filename
        else:
            return None
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None

def ConvertPdf(filename):
    if filename:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.insert_image(filename)
        pdf_filename = filename.replace('.tif', '.pdf')
        doc.save(pdf_filename)
        return pdf_filename
    else:
        return None

def Templades(pdf_filename):
    if pdf_filename:
        path = r'C:\Users\{}\Documents\Js\Bot\py\pdf'.format(getuser())
        os.makedirs(path, exist_ok=True)

        shutil.move(pdf_filename, os.path.join(path, pdf_filename))
        os.remove(pdf_filename.replace('.pdf', '.tif'))
    else:
        print("No se encontró el archivo PDF para aplicar la plantilla.")

def ConsultApi(ip, port, endpoint, key_data, suministro):
    # Verifica la caché primero
    # pdf_file = cache(suministro)
    # if pdf_file:
    #     return pdf_file
    
    # Si no se encuentra en la caché, procede con la solicitud
    url = f"http://{ip}:{port}/{endpoint}"

    data = {
        "suministro": suministro
    }

    data_bytes = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            result = json.loads(response_data)
            data_r = result.get(key_data)
            # Registrar la solicitud y la respuesta
            # log_request(suministro,data_r,filename='request_logs.json')
            if data_r is None:
                return 'suministro no existe en base de datos'
            return data_r
        
    except urllib.error.HTTPError as e:
        print(f'Error HTTP: {e.code} - {e.reason}')
    except urllib.error.URLError as e:
        print(f'Error URL: {e.reason}')
    
    return None








