import os
import sys
import time
import pandas as pd
from collections import OrderedDict
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

carNamesArr = {
    "אאודי":"Audi",
    "אברת\'":"Abarth",
    "אופל":"Opel",
    "איווייס":"Aiways",
    "אינפיניטי":"Infiniti",
    "איסוזו":"Isuzu",
    "אלפא רומיאו":"Alpha Romeo",
    "אם. ג\'י. / MG":"MG",
    "אסטון מרטין":"Aston-Martin",
    "ב.מ.וו":"BMW",
    "בנטלי":"Bently",
    "ביואיק":"Buick",
    "ג\'י.איי.סי/ GAC":"GAC",
    "ג\'ילי - Geely":"Geely",
    "ג\'יפ / Jeep":"Jeep",
    "ג\'נסיס":"Genesis",
    "גרייט וול":"GWM",
    "דאצ\'יה":"Dacia",
    "דודג\'":"Dodge",
    "דונגפנג":"Dongfeng",
    "די.אס / DS":"DS Automobiles",
    "דייהו":"Daewoo",
    "דייהטסו":"Daihatsu",
    "הונדה":"Honda",
    "הינו \ HINO":"Hino",
    "וולוו":"Volvo",
    "טויוטה":"Toyota",
    "טסלה":"Tesla",
    "יגואר":"Jaguar",
    "יונדאי":"Hyundai",
    "לאדה":"Lada",
    "לינקולן":"Lincolen",
    "לאנצ\'יה":"Lancia",
    "למבורגיני":"Lamborghini",
    "לנד רובר":"Land Rover",
    "לקסוס":"Lexus",
    "ליצ\'י":"Lichi",
    "לנצ\'יה":"Lancia",
    "מאזדה":"Mazda",
    "מזראטי":"Maserati",
    "מאן":"MAN",
    "מיני":"Mini",
    "מיצובישי":"Mitsubishi",
    "מקסוס":"Maxus",
    "מרצדס":"Mercedes-Benz",
    "ננג\'ינג":"Nanjing",
    "ניסאן":"Nisssan",
    "סאאב":"Saab",
    "סאנגיונג":"SsangYong",
    "סובארו":"Subaru",
    "סוזוקי":"Suzuki",
    "סיאט":"Seat",
    "סיטרואן":"Citroen",
    "סמארט":"Smart",
    "סקודה":"Skoda",
    "סרס / SERES":"Seres",
    "פולקסווגן":"Volkswagen",
    "פונטיאק":"Pontiac",
    "פורד":"Ford",
    "פורשה":"Porsche",
    "פיאט":"Fiat",
    "פיג\'ו":"Peugeot",
    "פרארי":"Ferrari",
    "קאדילק":"Cadillac",
    "קופרה":"Cupra",
    "קיה":"Kia",
    "קרייזלר":"Chrysler",
    "רובר":"Rover",
    "רנו":"Renault",
    "שברולט":"Chevrolet",
}

engineTypeArr = {
    "בנזין": "Benzene",
    "דיזל": "Diesel",
    "טורבו דיזל": "Turbo Diesel",
    "חשמל": "Electrical",
    "חשמלי": "Electrical",
    "היברידי": "Hybrid",
    "היברידי חשמל / דיזל": "Hybrid / Diesel",
    "היברידי חשמל / בנזין": "Hybrid / Benzene",
    "גט\"ד": "Gas",
    "גפ\"ם / בנזין": "Gas / Benzene",
    "גט\"ד / בנזין": "Gas / Benzene",
}

os.system('clear')
print("##############################")
print("#           SCRAPER          #")
print("##############################")

options = Options()
options.binary_location = r'/usr/bin/firefox-developer-edition'
options.set_preference('permissions.default.stylesheet', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driverRunning=False

def navigate(url):
    global driverRunning
    global driver
    while True:
        if (not driverRunning):
            options.headless = True
            options.set_preference('permissions.default.image', 2)
            driver = webdriver.Firefox(options=options)
        driver.get(url)
        if (driver.page_source.find("Captcha Digest:") != -1):
            driver.close()
            driverRunning=False
            print("Bot detected. Please solve the CAPTCHA")
            options.headless = False
            options.set_preference('permissions.default.image', 1)
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            input("Press Enter after solving to continue")
            driver.close()
        else:
            driverRunning=True
            break;

ans = "n"
if (not os.path.exists("NewCars.csv")):
    ans = "y"
else:
    ans = input("Do you want to rebuild new cars DB ? [y/N]: ")
if (ans == "y"):
    # create a list with car makers and page links respectively
    print("Scraping new cars...")
    navigate("https://pricelist.yad2.co.il/")
    carLinksList=[]
    for element in carNamesArr:
        carLinksList.append(carNamesArr[element])
        try:
            link = driver.find_element(By.LINK_TEXT, element).get_attribute('href')
            link = link.replace("NewCars.php", "search.php")
            carLinksList.append(link)
        except:
            carLinksList.pop()

    data_columns = ("Maker", "Year", "Model", "SubModel", "Gear", "Engine Type", "Engine Volume", "Horse Power", "Doors", "Seats", "Price")
    newCarsDF = pd.DataFrame(columns=data_columns)
    i=0
    currMaker=""
    for page in carLinksList:
        if (i % 2 == 0):
            currMaker=page
        else:
            # scraping each maker
            navigate(page)
            subModelLinks=[]
            elements = driver.find_elements(By.CLASS_NAME, "SubModelLink")
            for element in elements:
                subModelLinks.append(element.get_attribute('href'))
            for model in subModelLinks:
                navigate(model)
                currYear = driver.find_element(By.NAME, "Year").get_attribute('value')
                currModel = driver.find_element(By.NAME, "Model").get_attribute('value')
                currPrice = driver.find_element(By.NAME, "Price").get_attribute('value')
                currSubModel = driver.find_element(By.CLASS_NAME, "car_shortInfo").find_element(By.CLASS_NAME, 'value').text
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
                        "SubModel" : currSubModel,
                        "Gear" : currGear,
                        "Engine Type" : currEngineType,
                        "Engine Volume" : currVolume,
                        "Horse Power" : currHorse,
                        "Doors" : currDoors,
                        "Seats" : currSeats,
                        "Price" : currPrice }
                newCarsDF.loc[len(newCarsDF.index)] = row
                newCarsDF.to_csv('NewCars.csv')
        i=i+1

    print("Scraping the new cars DB is done")

# scraping old cars
ans = "n"
if (not os.path.exists("OldCars.csv")):
    ans = "y"
else:
    ans = input("Do you want to rebuild old cars DB ? [y/N]: ")
if (ans == "y"):
    print("Scraping old cars...")
    sinceYear = date.today().year - 10
    tillYear = date.today().year - 1
    oldCarsLinkList = [
        "https://pricelist.yad2.co.il/search.php?fromPrice=-1&toPrice=-1&fromYear=" + str(sinceYear)
                + "&toYear=" + str(tillYear) + "&carFamily%5B%5D=1&carFamily%5B%5D=2&carFamily%5B%5D=3",
        "https://pricelist.yad2.co.il/search.php?fromPrice=-1&toPrice=-1&fromYear=" + str(sinceYear)
                + "&toYear=" + str(tillYear) + "&carFamily%5B%5D=4&carFamily%5B%5D=5&carFamily%5B%5D=8",
        "https://pricelist.yad2.co.il/search.php?fromPrice=-1&toPrice=-1&fromYear=" + str(sinceYear)
                + "&toYear=" + str(tillYear) + "&carFamily%5B%5D=9&carFamily%5B%5D=6&carFamily%5B%5D=7",
    ]
    data_columns = ("Maker", "Year", "Model", "SubModel", "Gear", "Engine Type", "Engine Volume", "Horse Power", "Doors", "Seats", "Price")
    oldCarsDF = pd.DataFrame(columns=data_columns)

    p=1
    for link in oldCarsLinkList:
        navigate(link)
        print("[PHASE " + str(p) + "/" + str(len(oldCarsLinkList)) + "]")
        pageElements = driver.find_element(By.ID, "selectPage").find_elements(By.TAG_NAME, "option")
        pages = len(pageElements) - 1
        subModelLinks = []
        clear=False
        page=1
        while (page <= pages):
            if (page > 1):
                pageElements[page].click()
                time.sleep(1)
                try:
                    loadingElement = driver.find_element(By.CLASS_NAME, "loadingDiv")
                    while (loadingElement.is_displayed()):
                        time.sleep(1)
                except:
                    print("", end="\r")
                    sys.stdout.write("\033[K")
            subModelElements = driver.find_elements(By.CLASS_NAME, "SubModelLink")
            for element in subModelElements:
                subModelLinks.append(element.get_attribute('href'))
            if (clear):
                sys.stdout.write("\033[K")
            print("Scraped " + str(page) + "/" + str(pages) + " pages for submodels (" + str(len(subModelLinks)) + " links) " + str(round((page*100)/pages)) + "%", end="\r")
            clear=True
            pageElements = driver.find_element(By.ID, "selectPage").find_elements(By.TAG_NAME, "option")
            pages = len(pageElements) - 1
            page=page+1
        subModelLinks = list(OrderedDict.fromkeys(subModelLinks)) # de-dup
        count=len(subModelLinks)
        print("Scraping " + str(count) + " submodels")
        i=1
        clear=False
        for link in subModelLinks:
            navigate(link)
            currYear = driver.find_element(By.NAME, "Year").get_attribute('value')
            currPrice = driver.find_element(By.NAME, "Price").get_attribute('value')
            nameElements = driver.find_element(By.CLASS_NAME, "carName").find_elements(By.CSS_SELECTOR, '*')
            currSubModel = driver.find_element(By.CLASS_NAME, "car_shortInfo").find_element(By.CLASS_NAME, 'value').text
            currModel = nameElements[2].text
            currMaker = carNamesArr[nameElements[0].text]
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
                    "SubModel" : currSubModel,
                    "Gear" : currGear,
                    "Engine Type" : currEngineType,
                    "Engine Volume" : currVolume,
                    "Horse Power" : currHorse,
                    "Doors" : currDoors,
                    "Seats" : currSeats,
                    "Price" : currPrice }
            oldCarsDF.loc[len(oldCarsDF.index)] = row
            oldCarsDF.to_csv('OldCars.csv')
            if (clear):
                sys.stdout.write("\033[K")
            print("Scraped " + str(i) + "/" + str(count) + " submodels " + str(round((i*100)/count)) + "%", end="\r")
            clear=True
            i=i+1
        p=p+1
            
    print("Scraping the old cars DB is done")

# scraping used cars

ans = "n"
if (not os.path.exists("UsedCars.csv")):
    ans = "y"
else:
    ans = input("Do you want to rebuild used cars DB ? [y/N]: ")
if (ans == "y"):
    print("Scraping used cars...")
    data_columns = ("Maker", "Year", "Model", "SubModel", "Gear", "Engine Type", "Engine Volume", "Mileage", "Hand", "Ownership", "Previous Ownership", "Price")
    usedCarsDF = pd.DataFrame(columns=data_columns)
    link="https://www.yad2.co.il/vehicles/cars?priceOnly=1"
    navigate(link)
    pages = int(driver.find_element(By.CLASS_NAME, "numbers").find_elements(By.CSS_SELECTOR, "*")[9].text)
    print("found " + str(pages) + " pages of posts")
    skipNav=True
    # building a list of all post links
    postLinks = []
    clear=False
    for page in range(1, pages + 1):
        if (not skipNav):
            navigate(link + "&page=" + str(page))
        else:
            skipNav=False
        elements = driver.find_element(By.CLASS_NAME, "feed_list").find_elements(By.XPATH, "//div[contains(@id, 'feed_item_')]")
        for element in elements:
            pCode=str(element.get_attribute('item-id'))
            if (pCode == "None"):
                continue
            postLinks.append("https://www.yad2.co.il/item/" + pCode)
        if (clear):
            sys.stdout.write("\033[K")
        print("Scraped " + str(page) + "/" + str(pages) + " pages " + str(round((page*100)/pages)) + "%", end="\r")
        clear=True
    postLinks = list(OrderedDict.fromkeys(postLinks)) # de-dup
    print("Found " + str(len(postLinks)) + " posts")
    # foreach post link
    i=1
    clear=False
    for post in postLinks:
        navigate(post)
        found=False
        manCheck=driver.find_element(By.CLASS_NAME, "main_details").find_element(By.CLASS_NAME, "main_title").text
        currMaker=""
        currModel=""
        for man in carNamesArr:
            if (manCheck.find(man) != -1):
                currMaker=carNamesArr[man]
                currModel = manCheck.replace(man + " ", "")
                found=True
                break
        if (not found):
            continue
        detailsElement = driver.find_element(By.CLASS_NAME, "details_wrapper")
        currYear = int(driver.find_element(By.CLASS_NAME, "year-item").find_element(By.CLASS_NAME, 'value').text)
        currHand = int(driver.find_element(By.CLASS_NAME, "hand-item").find_element(By.CLASS_NAME, 'value').text)
        currVolume=0
        if (driver.page_source.find("סמ״ק") != -1):
            currVolume = int(driver.find_element(By.CLASS_NAME, "engine_size-item").find_element(By.CLASS_NAME, 'value').text.replace(",", ""))
        priceText = driver.find_element(By.CLASS_NAME, "price").text
        if (priceText.find("לחודש") != -1):
            continue
        currPrice = int(priceText.replace(" ₪", "").replace(",", ""))
        currSubModel = driver.find_element(By.CLASS_NAME, "second_title").text
        currMileage=0
        if (driver.page_source.find("more_details_kilometers") != -1):
            currMileage = detailsElement.find_element(By.ID, "more_details_kilometers").find_element(By.CSS_SELECTOR, "*").text
        currEngineType=""
        if (driver.page_source.find("more_details_engineType") != -1):
            currEngineType = engineTypeArr[detailsElement.find_element(By.ID, "more_details_engineType").find_element(By.CSS_SELECTOR, "*").text]
        currGear=True
        if (driver.page_source.find("more_details_gearBox") != -1):
            currGear = detailsElement.find_element(By.ID, "more_details_gearBox").find_element(By.CSS_SELECTOR, "*").text != "ידנית"
        currOwner=True
        if (driver.page_source.find("more_details_ownerID") != -1):
            currOwner = detailsElement.find_element(By.ID, "more_details_ownerID").find_element(By.CSS_SELECTOR, "*").text == "פרטית"
        prevOwner=True
        if (driver.page_source.find("more_details_previousOwner") != -1):
            prevOwner = detailsElement.find_element(By.ID, "more_details_previousOwner").find_element(By.CSS_SELECTOR, "*").text == "פרטית"
        row = {
            "Maker" : currMaker,
            "Year" : currYear,
            "Model" : currModel,
            "SubModel" : currSubModel,
            "Gear" : currGear,
            "Engine Type" : currEngineType,
            "Engine Volume" : currVolume,
            "Mileage" : currMileage,
            "Hand" : currHand,
            "Ownership" : currOwner,
            "Previous Ownership" : prevOwner,
            "Price" : currPrice }
        usedCarsDF.loc[len(usedCarsDF.index)] = row
        usedCarsDF.to_csv('UsedCars.csv')
        if (clear):
            sys.stdout.write("\033[K")
        print("Scraped " + str(i) + "/" + str(len(postLinks)) + " posts " + str(round((i*100)/len(postLinks))) + "%", end="\r")
        clear=True
        i=i+1

if (driverRunning):
    driver.close();
