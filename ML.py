import os
import sys
import time
import math
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import compose

def find_outliers_limit(df, col):
    q25 = np.percentile(df[col], 25)
    q75 = np.percentile(df[col], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5 # calculate the outlier cutoff
    lower = q25 - cut_off
    upper =  q75 + cut_off
    return lower, upper

def remove_outlier(df, col, upper, lower):
    return np.where(df[col] > upper, upper, np.where(df[col] < lower, lower, df[col]))

print()
print("Reading databases")
databases = []
databases.append(pd.read_csv('NewCars.csv', index_col=[0]))
databases.append(pd.read_csv('OldCars.csv', index_col=[0]))
databases.append(pd.read_csv('UsedCars.csv', index_col=[0]))
dbNames = [ "New", "Old", "Used" ]
outlierCols = [
    ["Engine Volume", "Horse Power"], # New
    ["Engine Volume", "Horse Power"], # Old
    ["Engine Volume", "Mileage"] # Used
]

for i, db in enumerate(databases):
    for col in outlierCols[i]:
        lower, upper = find_outliers_limit(db, col)
        db[col] = remove_outlier(db, col, upper, lower)
unifiedDB = pd.concat(databases, keys=dbNames)

while True:
    os.system('clear')
    print("##############################")
    print("#      MACHINE LEARNING      #")
    print("##############################")
    print("Total entries: " + str(len(unifiedDB)))
    print()
    print("Choose an action:")
    print("1. Train model")
    print("2. Guess a car price")
    print("q. Go back to main menu")
    ans = input("> ")
    print()

    if (ans == '1'):
        XCols = ["Maker", "Year", "Model", "SubModel", "Gear", "Engine Type", "Engine Volume", "Mileage", "Hand", "Ownership", "Previous Ownership", "Doors", "Seats"]
        XType = ["t"    , "n"   , "t"    , "x"       , "b"   , "t"          , "n"            , "n"      , "n"   , "b"        , "b"                 , "n"    , "n"]
        X = unifiedDB[XCols] # Input features
        Y = unifiedDB['Price'] # Prediction
        # normalizing data
        num_scaler = preprocessing.MinMaxScaler()
        cat_scaler = preprocessing.OrdinalEncoder()
        NCols = []
        TCols = []
        for i, col in enumerate(XCols):
            if (XType[i] == 'x'):
                continue
            if (XType[i] == 't'):
                TCols.append(col)
                continue
            NCols.append(col)
        trans = compose.ColumnTransformer(transformers = [
            ("num", num_scaler, NCols),
            ("cat", cat_scaler, TCols)],
            remainder="drop"
        )
        X = pd.DataFrame(trans.fit_transform(X), columns=trans.get_feature_names_out())
    elif (ans == '2'):
        time.sleep(1)
    elif (ans == 'q'):
        break # back to main menu
    else:
        print("Unrecognized option")
        time.sleep(5)
