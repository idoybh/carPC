import os
import requests
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from bs4 import BeautifulSoup as bs

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

# scraping the price list

purl="https://pricelist.yad2.co.il/"
rndVersion = random.randint(0,9223372036854775807)
agent = 'Mozilla/' + str(rndVersion) + ' (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
headers = {'User-Agent': agent}
newCarsUrls=()
pPage = requests.get(purl, headers=headers)
requests.session().cookies.clear()
pHTML = bs(pPage.text, 'html.parser')
r = pHTML.find_all('td', {'class': 'CarManufactur'})
print(pHTML)
