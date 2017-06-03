from urllib import request
import time
from  bs4 import BeautifulSoup as soup


v_page=0
count = 0
file = open("chick.csv","w")
file.write("contador" + ","+ "usuario" + "," + "marca" + "," + "producto" + "," + "texto" + ","  + "precioActual" + "," + "precioAnterior")
while v_page < 3000:
    v_page += 1
    print ("buscando en pagina:" , v_page)
    #urlpage = "https://www.chicfy.com/mas-nuevo/"+ str(v_page)
    #urlpage = "https://www.chicfy.com/user/antonialop/" + str(v_page)
    urlpage = "https://www.chicfy.com/tienda/" + str(v_page)
    #print (urlpage)
    #Abrimos la conexion y nos traemos la pagina
    uCliente = request.urlopen(urlpage)

    #metemos el contenido de la pagina en una variable
    #time.sleep(20)
    html_urlpage = uCliente.read()

    #cerramos la conexion
    uCliente.close()

    #parseamos el html con soup
    soup_urlpage = soup(html_urlpage, "html.parser", )
    #buscamos los divs que necesitamos (antes hemos inspeccionado los divs)
    gradas =  soup_urlpage.find_all("h4", {"class" : "grada"})
    containersL = soup_urlpage.find_all("div", {"class" : "left"})
    containersR = soup_urlpage.find_all("div", {"class": "right"})
    modelos = soup_urlpage.find_all("div", {"id": "social-links2"})

    for cL, cR, grada, modelo in zip(containersL,containersR, gradas, modelos) :
        count += 1
        marca = grada.text.encode("utf-8")
        producto = cL.a.text.encode("utf-8")
        texto = cL.p.text.encode("utf-8")
        precioactual = cR.div.text.encode("utf-8")
        precioanterior = cR.span.text.encode("utf-8")
        usuario = modelo.h5.a.text.encode("utf-8")

        file.write(str(count) + "," + str(usuario) + "," + str(marca) + "," + str(producto) + "," + str(texto) + ","  + str(precioactual.strip()) + "," + str(precioanterior.strip()))
        print(count, ",", usuario, ",", marca, "'", producto, ",", texto, ",", precioactual.strip(), ",",precioanterior.strip())
        # if "maison" in usuario.strip():
        #   print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #   print (count , ",", usuario, ",",  marca, "'", producto, ",", texto , ",", precioactual.strip(), ",", precioanterior.strip() )
        #   print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

file.close()