import os
import requests
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

carNamesArr = [
    ["אאודי","Audi"],
    ["אברת\'","Abarth"],
    ["אופל","Opel"],
    ["איווייס","Aiways"],
    ["אינפיניטי","Infiniti"],
    ["איסוזו","Isuzu"],
    ["אלפא רומיאו","Alpha Romeo"],
    ["אם. ג\'י. / MG","MG"],
    ["אסטון מרטין","Aston-Martin"],
    ["ב.מ.וו","BMW"],
    ["בנטלי","Bently"],
    ["ג\'י.איי.סי/ GAC","GAC"],
    ["ג\'ילי - Geely","Geely"],
    ["ג\'יפ / Jeep","Jeep"],
    ["ג\'נסיס","Genesis"],
    ["דאצ\'יה","Dacia"],
    ["דודג\'","Dodge"],
    ["דונגפנג","Dongfeng"],
    ["די.אס / DS","DS Automobiles"],
    ["הונדה","Honda"],
    ["הינו \ HINO","Hino"],
    ["וולוו","Volvo"],
    ["טויוטה","Toyota"],
    ["טסלה","Tesla"],
    ["יגואר","Jaguar"],
    ["יונדאי","Hyundai"],
    ["למבורגיני","Lamborghini"],
    ["לנד רובר","Land Rover"],
    ["לקסוס","Lexus"],
    ["מאזדה","Mazda"],
    ["מאן","MAN"],
    ["מיני","Mini"],
    ["מיצובישי","Mitsubishi"],
    ["מקסוס","Maxus"],
    ["מרצדס","Mercedes-Benz"],
    ["ניסאן","Nisssan"],
    ["סאנגיונג","SsangYong"],
    ["סובארו","Subaru"],
    ["סוזוקי","Suzuki"],
    ["סיאט","Seat"],
    ["סיטרואן","Citroen"],
    ["סמארט","Smart"],
    ["סקודה","Skoda"],
    ["סרס / SERES","Seres"],
    ["פולקסווגן","Volkswagen"],
    ["פורד","Ford"],
    ["פורשה","Porsche"],
    ["פיאט","Fiat"],
    ["פיג\'ו","Peugeot"],
    ["קאדילק","Cadillac"],
    ["קופרה","Cupra"],
    ["קיה","Kia"],
    ["קרייזלר","Chrysler"],
    ["רנו","Renault"],
    ["שברולט","Chevrolet"],
]

engineTypeArr = {
    "בנזין": "Benzene",
    "דיזל": "Diesel",
    "טורבו דיזל": "Turbo Diesel",
    "חשמל": "Electrical",
}

purl="https://pricelist.yad2.co.il/"

content = ""
while True:
    options = Options()
    options.binary_location = r'/usr/bin/firefox-developer-edition'
    options.headless = False # TODO: remove DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    driver = webdriver.Firefox(options=options)
    driver.get(purl)
    content = driver.page_source
    if (content.find("Captcha Digest:") != -1):
        print("Bot detected. Please solve the CAPTCHA")
        options.headless = False
        driver = webdriver.Firefox(options=options)
        driver.get(purl)
        input("Press Enter after solving to continue")
    else:
        break;
# create a list with car makers and page links respectively
carLinksList=[]
for element in carNamesArr:
    carLinksList.append(element[1])
    link = driver.find_element(By.LINK_TEXT, element[0]).get_attribute('href')
    link = link.replace("NewCars.php", "search.php")
    carLinksList.append(link)

data_columns = ("Maker", "Year", "Model", "Gear", "Engine Type", "Engine Volume", "Horse Power", "Doors", "Seats", "Price")
newCarsDF = pd.DataFrame(columns=data_columns)
i=0
currMaker=""
for page in carLinksList:
    if (i % 2 == 0):
        currMaker=page
    else:
        # scraping each maker
        driver.get(page)
        subModelLinks=[]
        elements = driver.find_elements(By.CLASS_NAME, "SubModelLink")
        for element in elements:
            subModelLinks.append(element.get_attribute('href'))
        for model in subModelLinks:
            driver.get(model)
            currYear = driver.find_element(By.NAME, "Year").get_attribute('value')
            currModel = driver.find_element(By.NAME, "Model").get_attribute('value')
            currPrice = driver.find_element(By.NAME, "Price").get_attribute('value')
            currGear = driver.find_element(By.NAME, "Price").get_attribute('value')
            generalDetails = driver.find_element(By.CLASS_NAME, "car_general_details")
            generalDetailsList = generalDetails.find_elements(By.CLASS_NAME, "value")
            j=1
            if ("תיבת הילוכים" in driver.page_source):
                currGear = generalDetailsList[j].text != "ידני"
                j=j+1
            else:
                currGear = ""
            if ("סוג מנוע" in driver.page_source):
                currEngineType = engineTypeArr[generalDetailsList[j].text]
                j=j+1
            else:
                currEngineType = ""
            if ("מספר דלתות" in driver.page_source):
                currDoors = int(generalDetailsList[j].text)
                j=j+1
            else:
                currDoors = 0
            if ("מספר מושבים" in driver.page_source):
                currSeats = int(generalDetailsList[j].text)
                j=j+1
            else:
                currSeats = 0
            if ("נפח מנוע" in driver.page_source):
                currVolume = int(generalDetailsList[j].text.replace(',', '').replace(" סמ\"ק", ""))
                j=j+1
            else:
                currVolume = 0
            if ("מספר כוחות סוס" in driver.page_source):
                currHorse = int(generalDetailsList[j].text.replace(" כ\"ס", ""))
                j=j+1
            else:
                currHorse = 0
            row = { "Maker" : currMaker,
                    "Year" : currYear,
                    "Model" : currModel,
                    "Gear" : currGear,
                    "Engine Type" : currEngineType,
                    "Engine Volume" : currVolume,
                    "Horse Power" : currHorse,
                    "Doors" : currDoors,
                    "Seats" : currSeats,
                    "Price" : currPrice }
            newCarsDF.loc[len(newCarsDF.index)] = row
            print(newCarsDF)
    i=i+1

print(newCarsDF)
driver.close();
