import os
import sys
import time
import math
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date

def find_outliers_limit(df, col):
    q25 = np.percentile(df[col], 25) # lowest 25 percentile
    q75 = np.percentile(df[col], 75) # highest 25 percentile
    iqr = q75 - q25 # middle half of all values
    cut_off = iqr * 1.5 # calculate the outlier cutoff
    lower = q25 - cut_off
    upper =  q75 + cut_off
    return lower, upper

def remove_outlier(df, col, upper, lower):
    # round all values out of bounds to the edges of it
    return np.where(df[col] > upper, upper, np.where(df[col] < lower, lower, df[col]))

def plot_avg_graph(db, dataList, dataLocStr, title, xLabel):
    # average price per model
    found = False
    selectedDB = db
    prices = []
    if ('New' in db.index or 'Old' in db.index):
        selectedDB = db.loc['New':'Old'] # plotting non used cars
        found = True
    while (True):
        ans = input("Select a year (2012-2022 or a = all): ")
        if (ans == 'a'):
            break
        if (ans.isnumeric() and int(ans) >= 2012 and int(ans) <= 2022):
            selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
            break
        print("Invalid input")
    if (found):
        ttlAverage = selectedDB['Price'].mean()        
        for item in dataList:
            prices.append(selectedDB.loc[selectedDB[dataLocStr] == item]['Price'].mean())
        plt.bar(dataList, prices)
        plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='b')

    foundUsed = False
    if ('Used' in db.index):
        selectedDB = db.loc['Used'] # plotting used
        foundUsed = True
        if (ans != 'a'):
            selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
        ttlAverage = selectedDB['Price'].mean()
        prices.clear()
        for item in dataList:
            prices.append(selectedDB.loc[selectedDB[dataLocStr] == item]['Price'].mean())
        plt.bar(dataList, prices, color='r', alpha=0.2)
        plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
    if (found or foundUsed):
        colors = { 'New':'blue', 'Used':'red', 'New avg':'blue', 'Used avg':'red' }
        labels = list(colors.keys())
        handles = []
        handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[0]]))
        handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[1]]))
        handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[2]], linestyle="--"))
        handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[3]], linestyle="--"))
        plt.xticks(rotation='vertical')
        plt.legend(handles, labels)
        plt.title(title)
        plt.xlabel(xLabel)
        plt.ylabel("Price")
        plt.show()

def plot_price_per_param_graph(db, axs, locStr, title, xLabel, kind = "bar",
        minVal = 0, rangeStart = -1, rangeEnd = -1, ticks = -1, rangeList = []):
    minV, maxV = rangeStart, rangeEnd
    if ((rangeStart == -1 or rangeEnd == -1) and len(rangeList) == 0):
        maxV = int(db[locStr].max())
        minV = int(db.loc[db[locStr] > minVal][locStr].min())
    vals = []
    prices = []
    if (len(rangeList) == 0):
        rangeList = range(minV, maxV + 1)
    for i in rangeList:
        val = db.loc[db[locStr] == i]['Price'].mean()
        if (np.isnan(val)):
            continue
        val = int(val)
        prices.append(val)
        if (len(rangeList) == 0):
            vals.append(int(i))
        else:
            vals.append(i)
    if (ticks > 0):
        axs.set_xticks(range(minV, maxV + 1, ticks))
    axs.set_title(title)
    axs.set_xlabel(xLabel)
    axs.set_ylabel("Price")
    if (kind == "bar"):
        axs.bar(vals, prices)
    elif (kind == "scatter"):
        axs.scatter(vals, prices, s=5)
        z = np.polyfit(vals, prices, 2)
        p = np.poly1d(z)
        axs.plot(vals, p(vals), c="red", alpha=0.6)
        colors = { 'New':'blue', 'Used':'red', 'New avg':'blue', 'Used avg':'red' }
        labels = [ "Trend" ]
        handles = [ ]
        handles.append(plt.Line2D((0,0),(1,1), color="red", alpha=0.6))
        axs.legend(handles, labels)
    elif (kind == "line"):
        axs.line(vals, prices)
    elif (kind == "plot"):
        axs.plot(vals, prices)

def plot_price_per_binary_graph(db, axs, dataList, locStr, title):
    prices = []
    prices.append(db.loc[db[locStr] == True]['Price'].mean())
    prices.append(db.loc[db[locStr] == False]['Price'].mean())
    axs.set_title(title)
    axs.set_ylabel("Price")
    axs.bar(dataList, prices)

def plot_value_graph(db, dataList, dataLocStr, title):
    # average price ; N/O Posts ; sum of all prices
    #       y       ;     x     ;      size
    ttlAverage = db['Price'].mean()
    maxSum = 0
    prices = []
    pricesSum = []
    posts = []
    colors = plt.cm.gist_ncar(np.linspace(0,0.9,len(dataList)))
    for item in dataList:
        curr = db.loc[db[dataLocStr] == item]['Price'].sum()
        if (curr > maxSum):
            maxSum = curr
    for item in dataList:
        pRows = db.loc[db[dataLocStr] == item]['Price']
        prices.append(pRows.mean())
        pricesSum.append((pRows.sum() / maxSum) * 2000)
        posts.append(len(db.loc[db[dataLocStr] == item]))
    plt.scatter(posts, prices, pricesSum, c=colors, alpha=0.4)
    plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
    handles = [plt.Line2D((0,0), (1,1), color='red', linestyle="--")]
    labels = ['average price']
    plt.legend(handles, labels)
    plt.title(title + "\nsize = sum of all prices")
    plt.xlabel("N/O Posts")
    plt.ylabel("Average Price")
    for i, item in enumerate(dataList):
        plt.annotate(item, (posts[i], prices[i]))
    plt.show()

print()
print("Reading databases")
databases = []
databases.append(pd.read_csv('NewCars.csv', index_col=[0]))
databases.append(pd.read_csv('OldCars.csv', index_col=[0]))
databases.append(pd.read_csv('UsedCars.csv', index_col=[0]))
dbNames = [ "New", "Old", "Used" ]
selected = [ True, True, True ]

ans = input("Round outliers? [Y/n]: ")
if (ans != 'n'):
    outlierCols = [
        ["Engine Volume", "Horse Power"], # New
        ["Engine Volume", "Horse Power"], # Old
        ["Engine Volume", "Mileage"] # Used
    ]

    for i, db in enumerate(databases):
        for col in outlierCols[i]:
            lower, upper = find_outliers_limit(db, col)
            db[col] = remove_outlier(db, col, upper, lower)

while True:
    os.system('clear')
    print("##############################")
    print("#        DATA ANALYZER       #")
    print("##############################")

    selectedStr = ""
    addcomma = False
    entries = 0
    active = []
    activeNames = []
    for i in range(0, len(databases)):
        if (selected[i]):
            entries += len(databases[i])
            active.append(databases[i])
            if (addcomma):
                selectedStr += ", "
            else:
                addcomma = True
            selectedStr += dbNames[i]
            activeNames.append(dbNames[i])
    unifiedDB = pd.concat(active, keys=activeNames)

    print("Currently selected databases: " + selectedStr)
    print("Total entries: " + str(entries))
    print()
    print("Choose an action:")
    print("1. Display default graphs")
    print("2. Display by maker")
    print("3. Display by model")
    print("e. Select databases")
    print("q. Go back to main menu")
    ans = input("> ")
    print()

    if (ans == '1'): # default graphs
        fig, axs = plt.subplots(2, 2) # figure n.o 1
        # Average price per manufacture year
        since = date.today().year - 10
        until = date.today().year
        plot_price_per_param_graph(unifiedDB, axs[0,0], 'Year', "Average price per make year", "Year", "plot",
                rangeStart=since, rangeEnd=until)

        # Average price per Mileage
        maxM = unifiedDB.loc[unifiedDB['Mileage'] > 0]['Mileage'].max()
        curr = 0
        mileages = []
        while (curr < maxM):
            curr += 50000
            mileages.append(curr)
        mileages.append(maxM)
        prices = []
        for mileage in mileages:
            avg = unifiedDB.loc[(unifiedDB['Mileage'] < mileage + 25000) & (unifiedDB['Mileage'] > mileage - 25000)]['Price'].mean()
            prices.append(avg)
        axs[0,1].set_title("Average price per mileage")
        axs[0,1].set_xlabel("Mileage")
        axs[0,1].set_ylabel("Price")
        axs[0,1].plot(mileages, prices)

        # Average price per horse power
        plot_price_per_param_graph(unifiedDB, axs[1,0], 'Horse Power', "Average price per horse power",
                                   "Horse Power", "scatter")

        # Average price per hand
        plot_price_per_param_graph(unifiedDB, axs[1,1], 'Hand', "Average price per horse power", "Hand", ticks=1)

        plt.show()

        fig, axs = plt.subplots(3, 2) # figure n.o 2
        # Average price per engine volume
        plot_price_per_param_graph(unifiedDB, axs[0,0], 'Engine Volume', "Average price per engine volume",
                                   "Engine Volume", "scatter")

        # Average price per gear type
        plot_price_per_binary_graph(unifiedDB, axs[0,1], ['Automatic','Manual'], 'Gear',
                                    "Average price per gear type")

        # Average price per previous ownership
        plot_price_per_binary_graph(unifiedDB.loc['Used'], axs[1,0], ['Private','Non-private'], 'Previous Ownership',
                                    "Average price per previous ownership")

        # Average price per current ownership
        plot_price_per_binary_graph(unifiedDB.loc['Used'], axs[1,1], ['Private','Non-private'], 'Ownership',
                                    "Average price per current ownership")

        # Average price per engine type
        types = unifiedDB['Engine Type'].dropna().drop_duplicates().to_list()
        types.sort()
        plot_price_per_param_graph(unifiedDB, axs[2,0], 'Engine Type', "Average price per engine type",
                                   "Engine Type", rangeList=types)

        plt.show()

        fig, axs = plt.subplots(1, 2)
        # Average price per n/o doors
        plot_price_per_param_graph(unifiedDB, axs[0], 'Doors', "Average price per N/O doors", "N/O Doors", ticks=1)

        # Average price per n/o seats
        plot_price_per_param_graph(unifiedDB, axs[1], 'Seats', "Average price per N/O seats", "N/O Seats", ticks=1)

        plt.show()

        # average prices per maker (new cars)
        # here we only want new cars
        subDB = unifiedDB.loc['New':'Old']
        # pick up a random year of making to show the data for
        rndYear = random.randint(since, until)
        subDB = subDB.loc[subDB['Year'] == rndYear]
        makers = subDB['Maker'].drop_duplicates().to_list()
        makers.sort()
        prices.clear()
        for maker in makers:
            prices.append(subDB.loc[subDB['Maker'] == maker]['Price'].mean())
        plt.bar(makers, prices)
        plt.xticks(rotation='vertical')
        plt.title("Average price per maker (" + str(rndYear) + ")")
        plt.xlabel("Maker")
        plt.ylabel("Price")
        plt.show()
        time.sleep(1)

        # number of posts per maker
        subDB = unifiedDB.loc['Used']
        makers = unifiedDB['Maker'].drop_duplicates().to_list()
        makers.sort()
        posts = []
        used = []
        for maker in makers:
            posts.append(len(unifiedDB.loc[unifiedDB['Maker'] == maker].index))
            used.append(len(subDB.loc[subDB['Maker'] == maker].index))
        colors = { 'New':'blue', 'Used':'red' }
        labels = list(colors.keys())
        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
        plt.xticks(rotation='vertical')
        plt.title("N.O Posts per maker")
        plt.xlabel("Makers")
        plt.ylabel("Posts")
        plt.legend(handles, labels)
        plt.bar(makers, posts)
        plt.bar(makers, used, color="red")
        plt.show()

        # !! using makers list from previous graphs !!
        plot_value_graph(unifiedDB, makers, 'Maker', "Maker estimated market value")

        # finally, but most importantly, show a correlation matrix
        cGraph = sns.heatmap(unifiedDB.corr(), annot=True, cmap="coolwarm")
        cGraph.set(title="Correlation matrix")
        plt.show()
        
    elif (ans == '2'): # by maker
        makers = unifiedDB['Maker'].drop_duplicates().to_list()
        makers.sort()
        print("Choose a maker:")
        for i, maker in enumerate(makers):
            print(str(i) + ". " + maker)
        maker = makers[int(input("> "))]
        subDB = unifiedDB.loc[unifiedDB['Maker'] == maker]

        models = subDB['Model'].drop_duplicates().to_list()
        models.sort()
        plot_avg_graph(subDB, models, 'Model', "Average price per model", "Model")
        plot_value_graph(subDB, models, 'Model', "Model estimated market value")

    elif (ans == '3'): # by model
        makers = unifiedDB['Maker'].drop_duplicates().to_list()
        makers.sort()
        print("Choose a maker:")
        for i, maker in enumerate(makers):
            print(str(i) + ". " + maker)
        maker = makers[int(input("> "))]
        subDB = unifiedDB.loc[unifiedDB['Maker'] == maker]

        models = subDB['Model'].drop_duplicates().to_list()
        models.sort()
        print("Choose a model:")
        for i, model in enumerate(models):
            print(str(i) + ". " + model)
        model = models[int(input("> "))]
        subDB = subDB.loc[subDB['Model'] == model]

        subModels = subDB['SubModel'].drop_duplicates().to_list()
        subModels.sort()
        plot_avg_graph(subDB, subModels, 'SubModel', "Average price per sub-model", "Price")
        plot_value_graph(subDB, subModels, 'SubModel', "Sub-Model estimated market value")

    elif (ans == 'e'): # edit
        valid = False
        while (not valid):
            for i in range(0, len(databases)):
                ans = input("Use " + dbNames[i] + " DB? [Y/n]: ")
                curr = ans != 'n' and ans != 'N'
                selected[i] = curr
                if (curr):
                    valid = True
            if (not valid):
                print("Please select at least one database")
        continue # back to top
    elif (ans == 'q'):
        break # back to main menu
    else:
        print("Unrecognized option")
        time.sleep(5)
