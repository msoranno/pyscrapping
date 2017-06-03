from urllib import request
import time
from  bs4 import BeautifulSoup as soup


v_page=0
count = 0
while v_page < 500:
    v_page += 1
    #print (v_page)
    urlpage = "https://www.chicfy.com/mas-nuevo/"+ str(v_page)
    #print (urlpage)
    #Abrimos la conexion y nos traemos la pagina
    uCliente = request.urlopen(urlpage)

    #metemos el contenido de la pagina en una variable
    #time.sleep(20)
    html_urlpage = uCliente.read()

    #cerramos la conexion
    uCliente.close()

    #parseamos el html con soup
    soup_urlpage = soup(html_urlpage, "html.parser")
    #buscamos los divs que necesitamos (antes hemos inspeccionado los divs)
    gradas =  soup_urlpage.find_all("h4", {"class" : "grada"})
    containersL = soup_urlpage.find_all("div", {"class" : "left"})
    containersR = soup_urlpage.find_all("div", {"class": "right"})
    modelos = soup_urlpage.find_all("div", {"id": "social-links2"})

    #print (len(containers))
    # containersRight = soup_urlpage.find_all("div", {"class": "right"})
    # print (containersLeft[0].a.text)
    # print(containersLeft[0].p.text)
    # print (containersRight[0].div())
    #
    # print ("--")
    # print (containersLeft[0])
    #print(containersR[0])
    for cL, cR, grada, modelo in zip(containersL,containersR, gradas, modelos) :
        count += 1
        marca = grada.text
        producto = cL.a.text
        texto = cL.p.text
        precioactual = cR.div.text
        precioanterior = cR.span.text
        usuario = modelo.h5.a.text

        if usuario.strip() == "Estrellita34":
         print (count , ",", usuario, ",",  marca, "'", producto, ",", texto , ",", precioactual.strip(), ",", precioanterior.strip() )
