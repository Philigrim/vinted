from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import time
import json
import os

if __name__ == "__main__":

    url = input("Nurodykite is kokio puslapio rinkti rubu linkus: ") 
    
    # rubuFailas - failo pavadinimas, i kuri bus surasyti rubu linkai
    itemuLinkai = "itemuLinkai.txt"
    
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    browser.maximize_window()

    maxi = 10
    i = 10
    while (i>0):
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(0.5)
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
        time.sleep(0.5)
        print(str(round((maxi-i)/maxi*100)) + "% DONE (LINKU RINKIMAS)")
        i = i - 1
        
    htmlClear = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()
    linksToClothes = htmlClear.find('div', {'class': 'feed-grid'}).findAll('a')

    f = open(itemuLinkai, "x")
    f = open(itemuLinkai, "a")
    for link in linksToClothes:
        f.write('https://new.vinted.lt' + link.get('href') + '\n')
        i=i+1
    f.close()

    print("100% DONE (LINKU RINKIMAS)")
    
    print("Surinkti: " + str(i) + " linkai\n\n\n")
    os.system('python infoRinkimas.py')