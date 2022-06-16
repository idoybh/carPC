import os
import sys
import time
import math
import keras
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn import preprocessing, compose
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from pickle import dump, load

MODEL_FILE_NAME = "model/model.h5"
ENCODER_FILE_NAME = "model/encoder.pkl"
SCALER_FILE_NAME = "model/scaler.pkl"

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

def norm_db(db, save=True, enc=None, sca=None):
    # normalizing data
    NCols = ['Year', 'Engine Volume', 'Horse Power', 'Mileage', 'Hand', 'Gear', 'Ownership', 'Previous Ownership', 'Price']
    TCols = ['Maker', 'Model', 'Engine Type']
    # taking care of non-common columns with nan values
    db['Horse Power'].fillna(0, inplace = True)
    db['Mileage'].fillna(0, inplace = True)
    db['Hand'].fillna(0, inplace = True)
    db['Engine Type'].fillna("Benzene", inplace = True)
    db['Ownership'].fillna(True, inplace = True)
    db['Previous Ownership'].fillna(True, inplace = True)
    db['Gear'].fillna(True, inplace = True)
    encoder = enc
    scaler = sca
    catDB = db[TCols]
    numDB = db[NCols]
    if (enc == None or sca == None):
        encoder = preprocessing.OrdinalEncoder()
        scaler = preprocessing.StandardScaler()
        catDB = pd.DataFrame(encoder.fit_transform(db[TCols]), columns=TCols)
        numDB = pd.DataFrame(scaler.fit_transform(db[NCols]), columns=NCols)
    else:
        catDB = pd.DataFrame(encoder.transform(db[TCols]), columns=TCols)
        numDB = pd.DataFrame(scaler.transform(db[NCols]), columns=NCols)
    if (save):
        if (not os.path.exists(ENCODER_FILE_NAME)):
            open(ENCODER_FILE_NAME, 'x')
        if (not os.path.exists(SCALER_FILE_NAME)):
            open(SCALER_FILE_NAME, 'x')
        # saving normalization rates for later use
        dump(encoder, open(ENCODER_FILE_NAME, "wb"))
        dump(scaler, open(SCALER_FILE_NAME, "wb"))
    X = pd.concat([numDB, catDB], axis=1)
    return X

def prep_db(db, save=True):
    X = norm_db(db, save)
    y = X['Price']
    X.drop('Price', axis=1, inplace=True)
    return X, y

def create_model(db):
    X, y = prep_db(db)
    # building a 4-layer neural net
    model = Sequential()
    model.add(Dense(16, input_dim=X.shape[1], activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='linear'))
    opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model, X, y

def load_model(db):
    print("Loading the model...")
    model = keras.models.load_model(MODEL_FILE_NAME)
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
            ans = input("Do you want to retrain the model (r = resume)? [r/y/N]: ")
        if (ans != 'y' and ans != 'r'):
            continue
        elif (ans == 'r'):
            resume = True
        model, X, y = create_model(unifiedDB)
        if (resume):
            model = load_model(unifiedDB)
            print("Current Loss: " + str(model.evaluate(X, y)))
        # training the model
        epoch_num = 30
        batches = 10
        ans = input("N.O Epochs to run [" + str(epoch_num) + "]: ")
        if (ans != '' and ans.isnumeric()):
            epoch_num = int(ans)
        print("Training...")
        X, X_test, y, y_test = train_test_split(X, y, test_size=0.15, shuffle=True)
        history = model.fit(
            X, y, validation_data=(X_test, y_test),
            verbose=1, epochs=epoch_num,
            batch_size=batches, shuffle=True
        )
        print("Loss: " + str(model.evaluate(X, y)))
        print("Done training, saving the last checkpoint")
        model.save(MODEL_FILE_NAME, save_format='h5')
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model History')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend()
        plt.show()
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
        isAutoGear = input("Automatic gear [Y/n]: ") != 'n'
        isPrivate = input("Private ownership [Y/n]: ") != 'n'
        isPrevPrivate = input("Previous private ownership [Y/n]: ") != 'n'

        data_cols = [ "Maker", "Year", "Model", "Gear", "Engine Volume", "Engine Type", "Horse Power", "Mileage", "Hand", "Ownership", "Previous Ownership", "Price" ]
        X = pd.DataFrame(columns=data_cols)
        X.loc[0] = {
            "Maker" : maker,
            "Year" : year,
            "Model" : model,
            "Gear" : isAutoGear,
            "Engine Type" : eType,
            "Engine Volume" : eVolume,
            "Horse Power": horse,
            "Mileage" : mileage,
            "Hand" : hand,
            "Ownership" : isPrivate,
            "Previous Ownership" : isPrevPrivate,
            "Price" : 0, # dummy value so pre-fit scaler won't get mad
        }

        scaler = load(open(SCALER_FILE_NAME, "rb"))
        encoder = load(open(ENCODER_FILE_NAME, "rb"))
        print("Summary:")
        print(X.drop('Price', axis=1))
        print()
        X = norm_db(X, save=False, enc=encoder, sca=scaler)
        X.drop('Price', axis=1, inplace=True)
        X['Price'] = ml_model.predict(X)
        NCols = ['Year', 'Engine Volume', 'Horse Power', 'Mileage', 'Hand', 'Gear', 'Ownership', 'Previous Ownership', 'Price']
        res = pd.DataFrame(scaler.inverse_transform(X[NCols]), columns=NCols).iloc[0]['Price']
        print("Predicted price is: " + str(round(res)))
        input("Press Enter to go back to the menu")

    elif (ans == '3' and modelExists):
        model = load_model(unifiedDB)
        X, y = prep_db(unifiedDB, False)
        res = model.predict(X)

        input("Press Enter to go back to the menu")
        
    elif (ans == 'q'):
        break # back to main menu
    else:
        print("Unrecognized option")
        time.sleep(5)
