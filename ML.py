import os
import sys
import time
import math
import keras
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OrdinalEncoder
from pickle import dump, load

MODEL_FILE_NAME = "model/model.h5"

if (not os.path.exists("model")):
    os.mkdir("model")

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

def print_mse(model, X, y):
    # The mean squared error
    mse = mean_squared_error(y, model.predict(X))
    print("Mean squared error (MSE): {:.4f}".format(mse))

def norm_db(db):
    # taking care of non-common columns with nan values
    db['Horse Power'].fillna(0, inplace = True)
    db['Mileage'].fillna(0, inplace = True)
    db['Hand'].fillna(0, inplace = True)
    db['Doors'].fillna(0, inplace = True)
    db['Seats'].fillna(0, inplace = True)
    db['Engine Type'].fillna("Benzene", inplace = True)
    db['Ownership'].fillna(True, inplace = True)
    db['Previous Ownership'].fillna(True, inplace = True)
    db['Gear'].fillna(True, inplace = True)
    # Handling categorical columns (and dropping irrelevant columns - no corr to price)
    encoder = OrdinalEncoder()
    NCols = ['Year', 'Engine Volume', 'Horse Power', 'Mileage', 'Hand', 'Gear', 'Ownership', 'Previous Ownership', 'Doors', 'Seats']
    TCols = ['Maker', 'Model', 'Engine Type']
    catDB = pd.DataFrame(encoder.fit_transform(db[TCols]), columns=TCols)
    numDB = db[NCols].reset_index(drop=True)
    X = pd.concat([catDB, numDB], axis=1)
    y = db['Price'].reset_index(drop=True)
    return X, y

def create_model(db, iter):
    X, y = norm_db(db)
    n_estimators = [5,7,11,15,20,40,50,70,100] # number of trees in the random forest
    max_features = [None, 'sqrt'] # number of features in consideration at every split
    max_depth = [int(x) for x in np.linspace(10, 120, num=12)] # maximum number of levels allowed in each decision tree
    max_depth.append(None)
    min_samples_split = [2, 6, 10] # minimum sample number to split a node
    min_samples_leaf = [1, 3, 4] # minimum sample number that can be stored in a leaf node
    bootstrap = [True, False] # method used to sample data points
    rnd_h_parameters = {
        'n_estimators': n_estimators,
        'max_features': max_features,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'bootstrap': bootstrap
    }
    model = ensemble.RandomForestRegressor()
    model_rnd = RandomizedSearchCV(
        estimator=model,
        param_distributions=rnd_h_parameters,
        n_iter=iter,
        verbose=2,
        n_jobs=-1
    )
    return model_rnd, X, y

def load_model(db):
    print("Loading the model...")
    model = load(open(MODEL_FILE_NAME, "rb"))
    X, y = norm_db(db)
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    print_mse(model, X_test, y_test)
    print("Model loaded")
    return model

def choose_list(db, locStr):
    items = db[locStr].drop_duplicates().to_list()
    items.sort()
    print("Choose a" + locStr.lower() + ": ")
    for i, item in enumerate(items):
        print(str(i) + ". " + str(item))
    item = items[int(input("> "))]
    subDB = db.loc[db[locStr] == item]
    return subDB, item

print()
print("Reading databases")
databases = []
databases.append(pd.read_csv('NewCars.csv', index_col=[0]))
databases.append(pd.read_csv('OldCars.csv', index_col=[0]))
databases.append(pd.read_csv('UsedCars.csv', index_col=[0]))
outlierCols = [
    ["Engine Volume", "Horse Power"], # New
    ["Engine Volume", "Horse Power"], # Old
    ["Engine Volume", "Mileage"] # Used
]

for i, db in enumerate(databases):
    for col in outlierCols[i]:
        lower, upper = find_outliers_limit(db, col)
        db[col] = remove_outlier(db, col, upper, lower)
unifiedDB = pd.concat(databases)

while True:
    modelExists = os.path.exists(MODEL_FILE_NAME)
    os.system('clear')
    print("##############################")
    print("#      MACHINE LEARNING      #")
    print("##############################")
    print("Total entries: " + str(len(unifiedDB)))
    print()
    print("Choose an action:")
    print("1. Train model")
    if (modelExists):
        print("2. Guess a car price")
        print("3. Evaluate model")
    print("q. Go back to main menu")
    ans = input("> ")
    print()

    if (ans == '1'):
        ans = "n"
        resume = False
        if (not modelExists):
            ans = "y"
        else:
            ans = input("Do you want to retrain the model? [y/N]: ")
        if (ans != 'y'):
            continue
        ans = input("How many tries? [200]: ")
        if (ans == '' or not ans.isnumeric()):
            ans = 200
        model, X, y = create_model(unifiedDB, int(ans))

        # training the model
        print("Training...")
        model.fit(X, y)
        best_p = model.best_params_
        print("Best hyper-parameters found: " + str(best_p))
        print("Training the best model")
        model = ensemble.RandomForestRegressor(
            n_estimators=best_p['n_estimators'],
            min_samples_split=best_p['min_samples_split'],
            min_samples_leaf=best_p['min_samples_leaf'],
            max_features=best_p['max_features'],
            max_depth=best_p['max_depth'],
            bootstrap=best_p['bootstrap'],
            n_jobs=-1,
            verbose=1,
        )
        model.fit(X, y)
        print("Done training. Saving the best model")
        dump(model, open(MODEL_FILE_NAME, "wb"))
        print_mse(model, X, y)
        input("Press Enter to go back to the menu")

    elif (ans == '2' and modelExists):
        ml_model = load_model(unifiedDB)

        subDB, maker = choose_list(unifiedDB, 'Maker')
        subDB, model = choose_list(subDB, 'Model')
        year = int(input("Year [2012-2022]: "))
        subDB, eType = choose_list(subDB, 'Engine Type')
        eVolume = int(input("Engine volume [cm³]: "))
        horse = int(input("Horse power: "))
        mileage = int(input("Mileage [km]: "))
        hand = int(input("N.O Hands: "))
        doors = int(input("N.O Doors: "))
        seats = int(input("N.O Seats: "))
        isAutoGear = input("Automatic gear [Y/n]: ") != 'n'
        isPrivate = input("Private ownership [Y/n]: ") != 'n'
        isPrevPrivate = input("Previous private ownership [Y/n]: ") != 'n'

        data_cols = [ "Maker", "Model", "Year", "Gear", "Engine Volume", "Engine Type", "Horse Power", "Mileage", "Hand", "Doors", "Seats", "Ownership", "Previous Ownership", "Price" ]
        X = pd.DataFrame(columns=data_cols)
        X.loc[0] = {
            "Maker" : maker,
            "Model" : model,
            "Year" : year,
            "Gear" : isAutoGear,
            "Engine Type" : eType,
            "Engine Volume" : eVolume,
            "Horse Power": horse,
            "Mileage" : mileage,
            "Hand" : hand,
            "Doors" : doors,
            "Seats" : seats,
            "Ownership" : isPrivate,
            "Previous Ownership" : isPrevPrivate,
            "Price" : 0, # dummy value so pre-fit scaler won't get mad
        }

        print("Summary:")
        print(X.drop('Price', axis=1))
        print()
        X, y = norm_db(X)
        X['Price'] = ml_model.predict(X)
        print("Predicted price is: " + str(round(X.loc[0]['Price'])))
        input("Press Enter to go back to the menu")

    elif (ans == '3' and modelExists):
        model = load_model(unifiedDB)
        X, y = norm_db(unifiedDB)
        X['Price'] = model.predict(X)

        # Show a plot comparing actual and predicted values
        plt.plot(np.arange(0, len(X), step=1), X['Price'])
        plt.plot(np.arange(0, len(y), step=1), y, c="green", alpha=0.5)
        plt.title("Model Evaluation")
        plt.ylabel('Price')
        plt.xlabel('Entry')
        colors = { 'Results':'blue', 'Actual':'green' }
        labels = list(colors.keys())
        handles = []
        for i, label in enumerate(labels):
            handles.append(plt.Line2D((0,0),(1,1), color=colors[labels[i]]))
        plt.legend(handles, labels)
        plt.show()

        # Show a plot of feature importances
        print("Computing feature importances")
        X.drop('Price', axis=1, inplace=True)
        importances = list(model.feature_importances_)
        features = []
        for col in X:
            features.append(col)
        plt.title("Feature importances")
        plt.ylabel("Importance")
        plt.xlabel("Feature")
        plt.xticks(rotation = 25)
        plt.bar(features, importances)
        plt.show()

        input("Press Enter to go back to the menu")
        
    elif (ans == 'q'):
        break # back to main menu
    else:
        print("Unrecognized option")
        time.sleep(5)
