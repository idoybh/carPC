import os
import sys
import time
import math
import pandas as pd

print()
print("Reading databases")
databases = []
databases.append(pd.read_csv('NewCars.csv', index_col=[0]))
databases.append(pd.read_csv('OldCars.csv', index_col=[0]))
databases.append(pd.read_csv('UsedCars.csv', index_col=[0]))
dbNames = [ "New", "Old", "Used" ]
unifiedDB = pd.concat(databases, keys=dbNames)



while True:
    os.system('clear')
    print("##############################")
    print("#      MACHINE LEARNING      #")
    print("##############################")
    print("Total entries (after outliers removal): " + str(len(unifiedDB)))
    print()
    print("Choose an action:")
    print("1. Train model")
    print("2. Guess a car price")
    print("q. Go back to main menu")
    ans = input("> ")
    print()

    if (ans == '1'):
        time.sleep(1)
    elif (ans == '2'):
        time.sleep(1)
    elif (ans == 'q'):
        break # back to main menu
    else:
        print("Unrecognized option")
        time.sleep(5)
