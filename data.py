import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    for i in range(0, len(databases)):
        if (selected[i]):
            entries += len(databases[i])
            if (addcomma):
                selectedStr += ", "
            else:
                addcomma = True
            selectedStr += dbNames[i]
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
        time.sleep(1)
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
