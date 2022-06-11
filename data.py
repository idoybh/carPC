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

    if (ans == '1'): # default graphs
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

        # Average price per hand
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

        # Average price per engine volume
        fig, axs = plt.subplots(2, 2)
        maxV = int(unifiedDB['Engine Volume'].max())
        minV = int(unifiedDB.loc[unifiedDB['Engine Volume'] > 0]['Engine Volume'].min())
        volumes = []
        prices.clear()
        for volume in range(minV, maxV + 1):
            volumes.append(volume)
            prices.append(unifiedDB.loc[unifiedDB['Engine Volume'] == volume]['Price'].mean())
        axs[0,0].set_title("Average price per engine volume")
        axs[0,0].set_xlabel("Engine Volume")
        axs[0,0].set_ylabel("Price")
        axs[0,0].scatter(volumes, prices, s=5)

        # Average price per gear type
        gears = [ 'Automatic', 'Manual' ]
        prices.clear()
        prices.append(unifiedDB.loc[unifiedDB['Gear'] == True]['Price'].mean())
        prices.append(unifiedDB.loc[unifiedDB['Gear'] == False]['Price'].mean())
        axs[0,1].set_title("Average price per gear type")
        axs[0,1].set_ylabel("Price")
        axs[0,1].bar(gears, prices)

        # Average price per previous ownership
        subDB = unifiedDB.loc['Used'] # only used cars have prev ownership
        ownerships = [ 'Private', 'non-private' ]
        prices.clear()
        prices.append(subDB.loc[subDB['Previous Ownership'] == True]['Price'].mean())
        prices.append(subDB.loc[subDB['Previous Ownership'] == False]['Price'].mean())
        axs[1,0].set_title("Average price per previous ownership")
        axs[1,0].set_ylabel("Price")
        axs[1,0].bar(ownerships, prices)

        # avg price by engine type
        types = unifiedDB['Engine Type'].dropna().drop_duplicates().to_list()
        types.sort()
        prices.clear()
        for eType in types:
            prices.append(unifiedDB.loc[unifiedDB['Engine Type'] == eType]['Price'].mean())
        axs[1,1].set_title("Average price per engine type")
        axs[1,1].set_ylabel("Price")
        axs[1,1].bar(types, prices)
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
        ttlAverage = unifiedDB['Price'].mean()
        colors = plt.cm.gist_ncar(np.linspace(0,0.9,len(makers)))
        pricesSum = []
        prices.clear()
        for maker in makers:
            pRows = unifiedDB.loc[unifiedDB['Maker'] == maker]['Price']
            pricesSum.append((pRows.sum() / maxP) * 200)
            prices.append(pRows.mean())
        plt.scatter(posts, prices, pricesSum, c=colors, alpha=0.4)
        plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
        handles = [plt.Line2D((0,0), (1,1), color='red', linestyle="--")]
        labels = ['average price']
        plt.legend(handles, labels)
        plt.title("Maker estimated market value\nsize = sum of all prices")
        plt.xlabel("N/O Posts")
        plt.ylabel("Average Price")
        for i, maker in enumerate(makers):
            plt.annotate(maker, (posts[i], prices[i]))
        plt.show()

    elif (ans == '2'): # by maker
        makers = unifiedDB['Maker'].drop_duplicates().to_list()
        makers.sort()
        print("Choose a maker:")
        for i, maker in enumerate(makers):
            print(str(i) + ". " + maker)
        maker = makers[int(input("> "))]
        subDB = unifiedDB.loc[unifiedDB['Maker'] == maker]

        # average price per model
        models = subDB['Model'].drop_duplicates().to_list()
        models.sort()
        prices = []
        found = False
        selectedDB = subDB
        if ('New' in subDB.index or 'Old' in subDB.index):
            selectedDB = subDB.loc['New':'Old'] # plotting non used cars
            found = True
        ans = input("Select a year (2012-2022 or a = all): ")
        if (ans != 'a'):
            selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
        if (found):
            ttlAverage = selectedDB['Price'].mean()        
            for model in models:
                prices.append(selectedDB.loc[selectedDB['Model'] == model]['Price'].mean())
            plt.bar(models, prices)
            plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='b')

        foundUsed = False
        if ('Used' in subDB.index):
            selectedDB = subDB.loc['Used'] # plotting used
            foundUsed = True
            if (ans != 'a'):
                selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
            ttlAverage = selectedDB['Price'].mean()
            prices.clear()
            for model in models:
                prices.append(selectedDB.loc[selectedDB['Model'] == model]['Price'].mean())
            plt.bar(models, prices, color='r', alpha=0.2)
            plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
        if (found or foundUsed):
            colors = { 'New':'blue', 'Used':'red', 'New avg':'blue', 'Used avg':'red' }
            labels = list(colors.keys())
            handles = []
            handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[0]]))
            handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[1]]))
            handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[2]], linestyle="--"))
            handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[3]], linestyle="--"))
            plt.legend(handles, labels)
            plt.title("Average price per model")
            plt.xlabel("Model")
            plt.ylabel("Price")
            plt.show()

        # average price ; N/O Posts ; sum of all prices
        #       y       ;     x     ;      size

        # !! using models list from previous graph !!
        ttlAverage = subDB['Price'].mean()
        maxP = subDB['Price'].max()
        prices.clear()
        pricesSum = []
        posts = []
        colors = plt.cm.gist_ncar(np.linspace(0,0.9,len(models)))
        for model in models:
            pRows = subDB.loc[subDB['Model'] == model]['Price']
            prices.append(pRows.mean())
            pricesSum.append((pRows.sum() / maxP) * 200)
            posts.append(len(subDB.loc[subDB['Model'] == model]))
        plt.scatter(posts, prices, pricesSum, c=colors, alpha=0.4)
        plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
        handles = [plt.Line2D((0,0), (1,1), color='red', linestyle="--")]
        labels = ['average price']
        plt.legend(handles, labels)
        plt.title("Model estimated market value\nsize = sum of all prices")
        plt.xlabel("N/O Posts")
        plt.ylabel("Average Price")
        for i, model in enumerate(models):
            plt.annotate(model, (posts[i], prices[i]))
        plt.show()
            
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

        # average price per sub-model
        subModels = subDB['SubModel'].drop_duplicates().to_list()
        subModels.sort()
        prices = []
        found=False
        selectedDB = subDB
        if ('New' in subDB.index or 'Old' in subDB.index):
            selectedDB = subDB.loc['New':'Old'] # plotting non used cars
            found = True
        ans = input("Select a year (2012-2022 or a = all): ")
        if (ans != 'a'):
            selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
        if (found):
            ttlAverage = selectedDB['Price'].mean()    
            for subModel in subModels:
                prices.append(selectedDB.loc[selectedDB['SubModel'] == subModel]['Price'].mean())
            plt.bar(subModels, prices)
            plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='b')

        foundUsed = False
        if ('Used' in subDB.index):
            foundUsed = True
            selectedDB = subDB.loc['Used'] # plotting used
            if (ans != 'a'):
                selectedDB = selectedDB.loc[selectedDB['Year'] == int(ans)]
            ttlAverage = selectedDB['Price'].mean()
            prices.clear()
            for subModel in subModels:
                prices.append(selectedDB.loc[selectedDB['SubModel'] == subModel]['Price'].mean())
            plt.bar(subModels, prices, color='r', alpha=0.2)
            plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
        if (foundUsed or found):
            colors = { 'New':'blue', 'Used':'red', 'New avg':'blue', 'Used avg':'red' }
            labels = list(colors.keys())
            handles = []
            handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[0]]))
            handles.append(plt.Rectangle((0,0),1,1, color=colors[labels[1]]))
            handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[2]], linestyle="--"))
            handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[3]], linestyle="--"))
            plt.legend(handles, labels)
            plt.title("Average price per sub-model")
            plt.xlabel("Sub-Model")
            plt.ylabel("Price")
            plt.show()

        # average price ; N/O Posts ; sum of all prices
        #       y       ;     x     ;      size

        # !! using subModels list from previous graph !!
        ttlAverage = subDB['Price'].mean()
        maxP = subDB['Price'].max()
        prices.clear()
        pricesSum = []
        posts = []
        colors = plt.cm.gist_ncar(np.linspace(0,0.9,len(subModels)))
        for subModel in subModels:
            pRows = subDB.loc[subDB['SubModel'] == subModel]['Price']
            prices.append(pRows.mean())
            pricesSum.append((pRows.sum() / maxP) * 200)
            posts.append(len(subDB.loc[subDB['SubModel'] == subModel]))
        plt.scatter(posts, prices, pricesSum, c=colors, alpha=0.4)
        plt.axhline(y=ttlAverage, linewidth=1, linestyle='--', color='r')
        handles = [plt.Line2D((0,0), (1,1), color='red', linestyle="--")]
        labels = ['average price']
        plt.legend(handles, labels)
        plt.title("Sub-Model estimated market value\nsize = sum of all prices")
        plt.xlabel("N/O Posts")
        plt.ylabel("Average Price")
        for i, subModel in enumerate(subModels):
            plt.annotate(subModel, (posts[i], prices[i]))
        plt.show()
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
