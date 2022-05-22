import os

import requests
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from bs4 import BeautifulSoup as bs

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
