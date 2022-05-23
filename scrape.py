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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

carNamesArr = [
    ["אאודי","Audi"],
    ["אברת\'","Abarth"],
    ["אופל","Opel"],
    ["איוויס","Aiways"],
    ["אינפיניטי","Infiniti"],
    ["איסוזו","Isuzu"],
    ["אלפא רומאו","Alpha Romeo"],
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
    ["מאזדה ","Mazda"],
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
    ["פולסווגן","Volkswagen"],
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

purl="https://pricelist.yad2.co.il/"
carUrlFormat="https://pricelist.yad2.co.il/search.php?ExceptionValue=%s&Exception=CarManufactur"

content=""
while True:
    options = Options()
    options.binary_location = r'/usr/bin/firefox-developer-edition'
    options.headless = True
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
print(content)
