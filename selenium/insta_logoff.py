import time, codecs
from selenium import webdriver


start_time = time.time()

driver = webdriver.Chrome("D:\PycharmProjects\chromedriver.exe")
driver.get("https://www.instagram.com/maisontxell/")
totalSeguidores = str(driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/span/span""").text)
print ("totalSeguidores: ", totalSeguidores)

driver.quit()
print ("Ha tardado: " , time.time()- start_time)