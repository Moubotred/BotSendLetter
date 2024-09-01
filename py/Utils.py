import argparse
import ResourceHub as Rb  # Asumiendo que Rb es un módulo que has importado

ip = 'localhost'
port = '5000'
endpoint = 'procesar_suministro'
key_data = 'result'

def apiUrl(sum_value):
    """
    Consulta la API si no hay un registro previo en el archivo JSON.
    """
    rs = Rb.ConsultApi(ip, port, endpoint, key_data, sum_value)    
    print(rs)

def apiDoc(sum_value):
    raw_url = Rb.ConsultApi(ip, port, endpoint, key_data, sum_value)    
    if raw_url.endswith('.pdf') or raw_url.startswith('https'):

        if raw_url.endswith('.pdf'):
            print(raw_url)

        elif raw_url.startswith('https'):
            url = Rb.UrlSubdoc(raw_url)
            filename = Rb.FileWebDownloads(url, sum_value)
            ff = Rb.ConvertPdf(filename)
            Rb.Templades(ff)
            print(ff)

    else:
        print(raw_url)

def main():
    parser = argparse.ArgumentParser(description="Herramienta de utilidad para procesar datos.")
    
    parser.add_argument('sum', type=str, help='Valor de suma o identificador.')
    parser.add_argument('--mode', type=str, choices=['apiUrl', 'apiDoc'], required=True,
                        help="Modo de operación: 'apiUrl' para consultar la API o verificar caché, 'apiDoc' para descargar y convertir.")

    args = parser.parse_args()

    if args.mode == 'apiUrl':
        apiUrl(args.sum)
    elif args.mode == 'apiDoc':
        apiDoc(args.sum)

if __name__ == '__main__':
    main()
    
