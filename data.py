import os
import sys
import time
import math
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

print()
print("Reading databases")
databases = []
databases.append(pd.read_csv('NewCars.csv', index_col=[0]))
databases.append(pd.read_csv('OldCars.csv', index_col=[0]))
databases.append(pd.read_csv('UsedCars.csv', index_col=[0]))
dbNames = [ "New", "Old", "Used" ]
selected = [ True, True, True ]

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

    if (ans == '1'):
        # average price per manufacture year
        fig, axs = plt.subplots(2, 2)
        years = []
        prices = []
        since = date.today().year - 10
        until = date.today().year
        for year in range(since, until + 1):
            years.append(year)
            prices.append(unifiedDB.loc[unifiedDB['Year'] == year]['Price'].mean())
        axs[0,0].set_title("Average price per make year")
        axs[0,0].set_xlabel("Year")
        axs[0,0].set_ylabel("Price")
        axs[0,0].plot(years, prices)

        # average price per Mileage
        maxM = unifiedDB.loc[unifiedDB['Mileage'] > 0]['Mileage'].max()
        curr = 0
        mileages = []
        while (curr < maxM):
            curr += 50000
            mileages.append(curr)
        mileages.append(maxM)
        prices.clear()
        for mileage in mileages:
            avg = unifiedDB.loc[(unifiedDB['Mileage'] < mileage + 25000) & (unifiedDB['Mileage'] > mileage - 25000)]['Price'].mean()
            prices.append(avg)
        axs[0,1].set_title("Average price per mileage")
        axs[0,1].set_xlabel("Mileage")
        axs[0,1].set_ylabel("Price")
        axs[0,1].plot(mileages, prices)

        # Average price per horse power
        maxH = int(unifiedDB['Horse Power'].max())
        minH = int(unifiedDB.loc[unifiedDB['Horse Power'] > 0]['Horse Power'].min())
        horses = []
        prices.clear()
        for horse in range(minH, maxH + 1):
            horses.append(horse)
            prices.append(unifiedDB.loc[unifiedDB['Horse Power'] == horse]['Price'].mean())
        axs[1,0].set_title("Average price per horse power")
        axs[1,0].set_xlabel("Horse Power")
        axs[1,0].set_ylabel("Price")
        axs[1,0].scatter(horses, prices, s=5)

        # average price per hand
        maxH = int(unifiedDB['Hand'].max())
        hands = []
        prices.clear()
        for i in range(0, maxH + 1):
            val = unifiedDB.loc[unifiedDB['Hand'] == i]['Price'].mean()
            if (val < 100 or math.isnan(val)):
                continue
            prices.append(val)
            hands.append(i)
        axs[1,1].set_title("Average price per hand")
        axs[1,1].set_xlabel("Hand")
        axs[1,1].set_ylabel("Price")
        axs[1,1].bar(hands, prices)
        fig.show()

        input("Press Enter to continue")

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
        plt.title("N.O Posts per maker")
        plt.xlabel("Makers")
        plt.ylabel("Posts")
        plt.legend(handles, labels)
        plt.bar(makers, posts)
        plt.bar(makers, used, color="red")
        plt.show()

        # average price ; N/O Posts ; sum of all prices
        #       y       ;     x     ;      size

        # !! using posts and makers lists from previous graphs !!
        maxP = unifiedDB['Price'].max()
        colors = plt.cm.gist_ncar(np.linspace(0,1,len(makers)))
        pricesSum = []
        prices.clear()
        for maker in makers:
            pRows = unifiedDB.loc[unifiedDB['Maker'] == maker]['Price']
            pricesSum.append((pRows.sum() / maxP) * 200)
            prices.append(pRows.mean())
        plt.scatter(posts, prices, pricesSum, c=colors, alpha=0.4)
        plt.title("Maker estimated market value\nsize = sum of all prices")
        plt.xlabel("N/O Posts")
        plt.ylabel("Average Price")
        for i, maker in enumerate(makers):
            plt.annotate(maker, (posts[i], prices[i]))
        plt.show()

    elif (ans == '2'):
        time.sleep(1)
    elif (ans == '3'):
        time.sleep(1)
    elif (ans == 'e'):
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
