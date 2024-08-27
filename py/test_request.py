import urllib.request
import concurrent.futures
import time
import ResourceHub as Rb

def enviar_solicitud(suministro):
    """
    Envía una solicitud HTTP POST al endpoint con el suministro especificado.
    
    Args:
        suministro: El valor del suministro a enviar en la solicitud.
    
    Returns:
        str: La respuesta del servidor.
    """
    try:
        ip = 'localhost'
        port = '4000'
        endpoint = 'procesar_suministro'
        key_data = 'result'
        rs = Rb.ConsultApi(ip,port,endpoint,key_data,suministro)
        return rs
    except Exception as e:
        return f"Error: {e}"

def test_concurrencia():
    """
    Realiza 300 solicitudes al endpoint, con algunas solicitudes concurrentes y otras secuenciales.
    """
    suministros = [1337534, 1337535, 1337536] * 5  # 300 suministros
    concurrentes = suministros[:100]  # Primeros 100 suministros serán enviados concurrentemente
    secuenciales = suministros[100:]  # Resto se enviará secuencialmente

    start_time = time.time()

    # Enviar solicitudes concurrentemente
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(enviar_solicitud, suministro) for suministro in concurrentes]
        concurrent_results = [future.result() for future in concurrent.futures.as_completed(futures)]

    print(f"Solicitudes concurrentes completadas en {time.time() - start_time:.2f} segundos.")

    # Enviar solicitudes secuenciales
    start_time = time.time()
    sequential_results = [enviar_solicitud(suministro) for suministro in secuenciales]
    
    print(f"Solicitudes secuenciales completadas en {time.time() - start_time:.2f} segundos.")

if __name__ == "__main__":
    # test_concurrencia()
    rs = enviar_solicitud(1337535)
    print(rs)
    
