from urllib import request
from datetime import datetime
from  bs4 import BeautifulSoup as soup
from elasticsearch import Elasticsearch


urlpage = "https://www.instagram.com/maisontxell/"
uCliente = request.urlopen(urlpage)
html_urlpage = uCliente.read()
uCliente.close()
soup_urlpage = soup(html_urlpage, "html.parser", )
dataCompleta = soup_urlpage.find_all("span", {"class" : "_bkw5z"})


#print(now)
#Quitamos los decimales con el replace en caso de que vengan
publicaciones=int(dataCompleta[0].text.replace(',' , ''))
seguidores=int(dataCompleta[1].text.replace(',' , ''))
seguidos=int(dataCompleta[2].text.replace(',' , ''))

doc = {
    'fecha': datetime.now(),
    'publicaciones': publicaciones,
    'seguidores': seguidores,
    'seguidos': seguidos
}

print(doc)

#hay que meter este docu en elastic

