# coding=utf-8
from urllib import request
from datetime import datetime
from  bs4 import BeautifulSoup as soup
from elasticsearch import Elasticsearch
import requests
from requests.auth import HTTPBasicAuth
import json , time

#------------------------------------------------------------
#Some Global Testing variables

# List instagram users to monitor
#usersToMonitor=["ronaldo"]
usersToMonitor=["maisontxell","katiapanteli"
				"_triatlon",
				"keepgoing_es",
				"chaneladdict123",
				"katyackermann",
				"mariu666",
				"iglesiasgabriela",
 				"msorannom"]

# Elasticsearch params
usarElastic=True  #False
elasticUser="user1"
elasticPass="123456"
elasticIP="localhost"
elasticPort="9200"
elasticurl="http://"+elasticIP+":"+elasticPort
elasticIndex="insta_index"
mappings = {
    'insta': {
        'properties': {
            'fecha': {'type': 'date'},
            'usuario': {'type': 'string'},
            'publicaciones': {'type': 'integer'},
            'seguidores': {'type': 'integer', },
            'seguidos': {'type': 'integer'},
        }
    }
}
body = {'mappings': mappings}

#end of globals
#------------------------------------------------------------




def testElasticConnection():

	""" Test the conecction wie ES before do anything """
	#verificamos que este ejecutandose
	try:
		res = requests.get(elasticurl, auth=HTTPBasicAuth(elasticUser, elasticPass))
		if res.status_code == 200:
			#print("Elastic esta vivo.")
			return True
		else:
			return False
			#print ("Error de conexión:")
			#print(res.content)
	except:
		#print("ostionsss")
		return False



def getNextValueID(mydict):

	"""Return the nex value available for insert a new document."""

    #Nos quedamos solo con los valores de los IDs para 
    #meterlos en un lista y determinar el mayor.

	totalIDs=mydict['hits']['total']
	proximoID=int(totalIDs)+1
	#print(mydict)
	#listaIDs=[]
	# for k,v in mydict.items():
	# 	myID=v['total'])
	# 	listaIDs.append(int(myID))

	# print(listaIDs)		
	# mayorEnLista=max(listaIDs)
	
	return proximoID
	
def checkValues(valor):

	""" This function check for values like 1.6m , 110K , etc and transform them to real values. """
	newvalor=""
	#print ("me ha llegado: ", valor)
	letra = valor[-1]
	if letra == 'k':
		#print ("estoy en la k")
		finddot = valor.find(".")
		if finddot >=0 :
			#print ("estoy en el dot", finddot)
			solovalor = len(valor) - 1
			newvalor = valor[0:solovalor] + "00"
			newvalor = newvalor.replace('.' , '')
		else:
			#print ("estoy fuera del dot")
			solovalor = len(valor) - 1
			newvalor = valor[0:solovalor] + "000"
	elif letra == 'm':
		#print ("estoy en la m")
		finddot = valor.find(".")
		if finddot >=0 :
			#print ("estoy en el dot", finddot)
			solovalor = len(valor) - 1
			newvalor = valor[0:solovalor] + "000000"
			newvalor = newvalor.replace('.' , '')
		else:
			#print ("estoy fuera del dot")
			solovalor = len(valor) - 1
			newvalor = valor[0:solovalor] + "000000"
	else:
		newvalor = valor

	return int(newvalor)
	
def main_noElastic():
	""" Main course """

	# Comienza el trabajo por usuarios a monitorizar
	i = 0
	for usuario in usersToMonitor:
		print('-----usuario: ' + usuario)
		time.sleep(5)
		i += 1
		urlpage = "https://www.instagram.com/" + usuario + "/"
		uCliente = request.urlopen(urlpage)
		html_urlpage = uCliente.read()
		uCliente.close()
		soup_urlpage = soup(html_urlpage, "html.parser", )

		#---------
		# Recogemos Followers
		#---------
		#Esto recoge la seccion del script numero 2
		data_string = soup_urlpage.findAll('script')[1].string.encode('utf8')
		#Esto separa la mierdaca del verdadero jason
		pre_followers = str(data_string).split('"followed_by": {"count":')[1]
		post_followers = str(pre_followers).split('}, "followed_by_viewer')[0]
		print('followers: ' + post_followers)

		#---------
		# Recogemos followed by y posts
		#---------
		meta_data = soup_urlpage.find("meta", property="og:description")
		pre_folloed_by2 = str(meta_data).split('Followers,')[1]
		post_folloed_by = str(pre_folloed_by2).split('Following,')[0]
		print('Followed_by: ' + post_folloed_by)
		pre_posts = str(meta_data).split('Following,')[1]
		pre_posts2 = str(pre_posts).split('Posts')[0]
		print('Posts: ' + pre_posts2)


def main():

	""" Main course """

	recienCreadoIndex=False
	elasticConnect="CONNKO"
	elasticIndexCreated="newIndex"
	publicaciones=0
	seguidores=0
	seguidos=0
	usuario="nadie"
	nextID=1
	now=datetime.now()

	if testElasticConnection():
		elasticConnect="CONNOK"
		#Conectamos con elastic y creamos el indice si no existe.
		es = Elasticsearch([{'host': elasticIP, 'port': elasticPort}], http_auth=(elasticUser, elasticPass))
		if es.indices.exists(index=elasticIndex):
			#print("El indice existe.")
			elasticIndexCreated="IndexExist"
		else:
			#print("El indice NO existe, lo creamos.")
			elasticIndexCreated="newIndex"
			creaIndex = es.indices.create(index=elasticIndex, ignore=400, body=body)
			recienCreadoIndex=True
			#creaIndex = es.indices.create(index=elasticIndex, ignore=400)


		#Comienza el trabajo por usuarios a monitorizar
		i=0
		for usuario in usersToMonitor:
			time.sleep(5)
			i += 1   
			urlpage = "https://www.instagram.com/"+usuario+"/"
			uCliente = request.urlopen(urlpage)
			html_urlpage = uCliente.read()
			uCliente.close()
			soup_urlpage = soup(html_urlpage, "html.parser", )

			# dataCompleta = soup_urlpage.find_all("span", {"class" : "_bkw5z"})

			# # The followers filed use 'title' to hide the real value
			# # here we extract this field.
			# for item in dataCompleta:
			# 	if str(item).find('title') >= 0:
			# 		#print(item['title'])
			# 		followersTittle = item['title']
			# 	else:
			# 		pass

			 
			# #print(now)
			# # ------ remove dots and commas

			# # - working publicaciones
			# publicaciones=dataCompleta[0].text.replace(',' , '')

			# # - working followers
			# #seguidores=dataCompleta[1].text.replace(',' , '')
			# seguidores_v1=followersTittle.replace(',' , '')
			# seguidores_v2=seguidores_v1.replace('.' , '')
			# seguidores=seguidores_v2

			# # - working follow
			# seguidos=dataCompleta[2].text.replace(',' , '')
			# # --------------------------------------------------


			#---------
			# Recogemos Followers
			#---------
			#Esto recoge la seccion del script numero 2
			data_string = soup_urlpage.findAll('script')[1].string.encode('utf8')
			#Esto separa la mierdaca del verdadero jason
			pre_followers = str(data_string).split('"followed_by": {"count":')[1]
			post_followers = str(pre_followers).split('}, "followed_by_viewer')[0]
			#print('followers: ' + post_followers)

			#---------
			# Recogemos seguidos  y posts
			#---------
			meta_data = soup_urlpage.find("meta", property="og:description")
			pre_seguidos = str(meta_data).split('Followers,')[1]
			post_seguidos = str(pre_seguidos).split('Following,')[0]
			#print('Followed_by: ' + post_seguidos)
			pre_posts = str(meta_data).split('Following,')[1]
			pre_posts2 = str(pre_posts).split('Posts')[0]
			#print('Posts: ' + pre_posts2)

			# --
			# quitamos las comas de los valores
			pre_posts2_v1=pre_posts2.replace(',' , '')
			post_followers_v1=post_followers.replace(',' , '')
			post_seguidos_v1=post_seguidos.replace(',' , '')

			# ------ check for special characters
			#Vamos a tratar de averiguar si vienen cosas raras en los valores
			#como 1.6m (1.600.000) o 130k (130.000)
			publicaciones = checkValues(str(pre_posts2_v1))
			seguidores = checkValues(str(post_followers_v1))
			seguidos = checkValues(str(post_seguidos_v1))
			# ----------------------------------------------------


			# -- Filling the document
			doc = {
			    'fecha': now,
			    'usuario': usuario,
			    'publicaciones': publicaciones,
			    'seguidores': seguidores,
			    'seguidos': seguidos
			}

			# -- Insertion wheter is a new creation index or not.
			if recienCreadoIndex:
				#si el indice esta recien creado insertamos directamente con id=1
				es.create(index=elasticIndex, doc_type='instsa', id=nextID, body=doc)
				print("insertado ", elasticIndexCreated, elasticConnect, nextID, "fecha:",now, "usuario:",usuario, "publicaciones:",publicaciones,"seguidores:", seguidores,"seguidos:", seguidos)
				recienCreadoIndex=False
				elasticIndexCreated="IndexExist"
			else:
				#dictIDs = es.search(index=elasticIndex, filter_path=['hits.hits._id'])
				dictIDs = es.search(index=elasticIndex, filter_path=['hits.total'])
				#print(dictIDs.items())
				nextID=getNextValueID(dictIDs)
				es.create(index=elasticIndex, doc_type='instsa', id=nextID, body=doc)
				print("insertado ", elasticIndexCreated, elasticConnect, nextID, "fecha:",now, "usuario:",usuario, "publicaciones:",publicaciones,"seguidores:", seguidores,"seguidos:", seguidos)

				#break
	else:
		print("Error ", elasticIndexCreated, elasticConnect, nextID, "fecha:",now, "usuario:",usuario, "publicaciones:",publicaciones,"seguidores:", seguidores,"seguidos:", seguidos)

if __name__ == "__main__":
	#print("----start----")
	#print(datetime.now())
	#print("....is being run directly")
	if usarElastic:
		main()
	else:
		main_noElastic()
	#print("----end----")
else:
    print("....is being imported into another module")
