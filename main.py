from urllib import request
import time
from  bs4 import BeautifulSoup as soup


#vcallChannel = "http://www.vestiairecollective.es/novedades/"

v_page=0
count = 0
while v_page < 180:
    v_page += 60
    print (v_page)
    vcallChannel = "http://www.vestiairecollective.es/novedades/#_=catalog&limit="+str(v_page)+"&priceMin=0&priceMax=38100&step=60"
    print (vcallChannel)
    #Abrimos la conexion y nos traemos la pagina
    uCliente = request.urlopen(vcallChannel)

    #metemos el contenido de la pagina en una variable
    time.sleep(20)
    html_vcallChannel = uCliente.read()

    #cerramos la conexion
    uCliente.close()

    #parseamos el html con soup
    soup_vcallChannel = soup(html_vcallChannel, "html.parser")

    #buscamos los divs que necesitamos (antes hemos inspeccionado los divs)
    containers = soup_vcallChannel.find_all("div", {"class" : "col-xs-6 col-sm-4"})

    for container in containers:
        count += 1
        marca = container.a["data-brand"]
        pid   = container.a["data-id"]
        precio = container.a["data-price"]
        titulo = container.a["data-title"]
        print (count, ")", marca, ",", pid , ",",  precio, ",",  titulo )