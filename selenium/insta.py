import random
from urllib import request
import time, codecs
from  bs4 import BeautifulSoup as soup
from selenium import webdriver


start_time = time.time()

#Login process
driver = webdriver.Chrome("D:\PycharmProjects\chromedriver.exe")
driver.get("https://www.instagram.com/msorannom/followers")
time.sleep(5)
user=driver.find_element_by_css_selector('[name="username"]')
user.send_keys('msorannom')
passw=driver.find_element_by_css_selector('[name="password"]')
passw.send_keys('pass de instagram')
login=driver.find_element_by_css_selector('[class="_ah57t _84y62 _i46jh _rmr7s"]')
login.click()

#Vamos al perfil
time.sleep(3)
#driver.find_element_by_css_selector('[class="_bkw5z]').click()
#driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/ul""").click()
driver.find_element_by_css_selector("a._s53mj > span._bkw5z").click()
time.sleep(2)

seguidores = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
#find number of followers
totalSeguidores = int(driver.find_element_by_xpath("//li[2]/a/span").text)
print ("totalSeguidores: ", totalSeguidores)

#bajamos la pagina hasta llegar al final del todooo
for i in range(int(totalSeguidores/2)):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", seguidores)
    time.sleep(random.randint(500,1000)/1000)
    print("Obteniendo seguidores %",round((i/(totalSeguidores/2)*100),2),"from","%100")

#Teniendo dodo cargado ahora si buscamos a la peña.
for j in range(int(totalSeguidores)):
    j += 1
    persona = driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/div[2]/ul/li["""+ str(j) +"""]/div/div[1]/div/div[2]""").text
    usuario = driver.find_element_by_xpath("""/html/body/div[2]/div/div[2]/div/div[2]/ul/li["""+ str(j) +"""]/div/div[1]/div/div[1]/a""").text
    print (totalSeguidores,"##",usuario,"##", persona)

driver.quit()

print ("Ha tardado: " , time.time()- start_time)