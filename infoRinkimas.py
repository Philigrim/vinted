import json
import os
import requests
from bs4 import BeautifulSoup
import urllib
import shutil
import random

if __name__ == "__main__":

    # failas - failo pavadinimas, is kurio imami rubai
    failas = "itemuLinkai.txt"
    
    rubuLinkai = open(failas, 'r') 
    linkai = rubuLinkai.readlines() 

    number = 1
    isviso = len(linkai)
    for url in linkai:
        failas = "data.json"

        response = requests.get(url)
        html = BeautifulSoup(response.text, 'lxml')

        category = []
        itemLocation = html.find_all(itemscope='itemscope')
        for location in itemLocation[1:]:
            category.append(location.text)

        infoDiv = html.find('div', {'class': 'box box--item-details'})

        price = infoDiv.find('div', {'class': 'c-text--heading c-text--left c-text'}).text.split()[0].replace(',','.')

        try:
            if(infoDiv.select_one('div[class^="details-list__item-title"]').text != None):
                brand = infoDiv.select_one('span[itemprop^="name"]').text
        except:
                brand = "Be prekės ženklo"
        
        if(infoDiv.find('div', {'class': 'details-list__item-title'}).text == "Dydis"):
            size = infoDiv.find('div', {'details-list__item-value'}).text.strip()
        else:
            if(infoDiv.find('div', {'class': 'details-list__item-title'}).find_next('div', {'class': 'details-list__item-title'}).text == "Dydis"):
                size = infoDiv.find('div', {'details-list__item-value'}).find_next('div', {'details-list__item-value'}).text.strip()
            else:
                size = "Nenurodyta"
                
        condition = infoDiv.find('div', {'itemprop': 'itemCondition'}).text.strip()
        color = infoDiv.find('div', {'itemprop': 'color'}).text

        titleAndDescription = json.loads(infoDiv.find('script', {'class': 'js-react-on-rails-component'}).contents[0])
        title = titleAndDescription["content"]["title"].strip()
        description = titleAndDescription["content"]["description"]

        details = {}
        details["Link"] = url
        details["Category"] = category
        details["Price"] = price
        details["Brand"] = brand
        details["Size"] = size
        details["Condition"] = condition
        details["Color"] = color
        details["Title"] = title
        details["Description"] = description

        path = os.getcwd() + "\\" + str(number) + ". " + details["Title"].replace("/", " ")
        os.mkdir(path)
        
        photosDiv = html.find('div', {'class': 'item-photos'})
        i = 0
        for a in photosDiv.find_all(href=True):
            i = i + 1
            imagesrc = a['href']
            imageName = str(i) + ".jpg"
            urllib.request.urlretrieve(imagesrc, imageName)
            shutil.move(imageName, path)

        details["Nuotraukos"] = i

        with open("data.json", 'w', encoding='utf-8') as outputFile:
            json.dump(details, outputFile, ensure_ascii=False, indent=4)

        shutil.move(failas, path)
        shutil.copyfile("ikeltiItem.py", path + "\\ikeltiItem.py")
        
        print(str(round(number/isviso*100)) + "% DONE (INFO RINKIMAS)")
        number = number + 1
    input("Baigta")