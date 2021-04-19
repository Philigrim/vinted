from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import os

import time
import json
import shutil

from selenium.webdriver.firefox.webdriver import FirefoxProfile

if __name__ == "__main__":
    profile = FirefoxProfile('C:\\Users\\Valdelio\'\\AppData\\Roaming\\mozilla\\Firefox\\Profiles\\a4g555yp.default-release')
    
    path = os.getcwd() + "\\"

    with open(path+'data.json', encoding='utf8') as json_file:
        data = json.load(json_file)

    browser = webdriver.Firefox(profile)

    #browser.get(data["Link"])
    #browser.find_element_by_xpath("//*[contains(text(), 'Pašalinti' )]").click()
    #browser.find_element_by_xpath("//*[contains(text(), 'Patvirtinti ir ištrinti' )]").click()
    
    browser.get('https://new.vinted.lt/items/new')
    browser.maximize_window()
    #browser.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
    htmlClear = BeautifulSoup(browser.page_source, 'lxml')

    i = 1
    while (i <= data["Nuotraukos"]):
        browser.find_element_by_xpath("//input[@type='file']").send_keys(path + str(i) + '.jpg')
        time.sleep(0.75)
        i = i + 1
    
    element = browser.find_element_by_class_name('c-tabs__content')
    browser.execute_script("""var element = arguments[0]; element.parentNode.removeChild(element);""", element)
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)

    browser.find_element_by_id('title').send_keys(data["Title"])
    browser.find_element_by_id('description').send_keys(data["Description"])

    browser.find_element_by_xpath("//input[@id='catalog_id']").click()

    if(data["Category"][0] == "Moterims"):
        element = browser.find_element_by_xpath("//div[@data-icon-name='dress']")
    elif(data["Category"][0] == "Vyrams"):
        element = browser.find_element_by_xpath("//div[@data-icon-name='tshirt']")
    elif(data["Category"][0] == "Vaikams"):
        element = browser.find_element_by_xpath("//div[@data-icon-name='kid-face']")
    else:
        element = browser.find_element_by_xpath("//div[@data-icon-name='house']")
    browser.execute_script("arguments[0].click();", element)

    try:
        i = 1
        while(i < len(data["Category"])):
            element = browser.find_element_by_xpath("//div[contains(@class, 'Cell_title__1gULu') and contains(., '" + data["Category"][i] + "')]")
            browser.execute_script("arguments[0].click();", element)
            i = i + 1
    except:
        pass
    
    browser.find_element_by_id('brand_id').send_keys(data["Brand"])
    browser.find_element_by_xpath("//input[@id='brand_id']").click()
    browser.find_element_by_xpath("//*[contains(text(), '" + data["Brand"] + "' )]").click()

    if(data["Size"] != "Nenurodyta"):
        browser.find_element_by_xpath("//input[@id='size_id']").click()
        browser.find_element_by_xpath("//div[contains(@class, 'Cell_title__1gULu') and contains(text(), '" + data["Size"] + "' )]").click()
        
    browser.find_element_by_xpath("//input[@id='color']").click()
    for color in data["Color"].split(", "):
        browser.find_element_by_xpath("//*[contains(text(), '" + color.capitalize() + "' )]").click()
    browser.find_element_by_xpath("//input[@id='status_id']").click()
    browser.find_element_by_xpath("//*[contains(text(), '" + data["Condition"] + "' )]").click()

    browser.find_element_by_id('price').send_keys(data["Price"])

    browser.find_element_by_xpath("//*[contains(text(), 'Išsaugoti ruošinį' )]").click()
    #browser.find_element_by_xpath("//*[contains(text(), 'Pridėti' )]").click()
    
    browser.close()