import os

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from bs4 import BeautifulSoup as bs

# scraping the price list

purl="https://pricelist.yad2.co.il/"
newCarsUrls=()
pPage = requests.get(purl)
pHTML = bs(pPage.text, 'html.parser')
r = pHTML.find_all('td', {'class': 'CarManufactur'})
print(r)
