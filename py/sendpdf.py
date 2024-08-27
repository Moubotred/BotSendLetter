import ResourceHub as Rb
import sys

sum = sys.argv[1]
# frame,suministro = Rb.SearchFileWeb(sum)
# suburl = Rb.UrlSubdoc(frame)
# filename = Rb.FileWebDownloads(suburl,suministro)
# ff = Rb.ConvertPdf(filename)
# Rb.Templades()

ip = '192.168.1.109'
port = '5000'
endpoint = 'search'
key_data = 'url'
raw_url = Rb.ConsultApi(ip,port,endpoint,key_data,sum)
url = Rb.UrlSubdoc(raw_url)
filename = Rb.FileWebDownloads(url,sum)
ff = Rb.ConvertPdf(filename)
Rb.Templades(ff)
print(ff)