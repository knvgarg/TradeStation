# from google.colab import drive
# drive.mount("/content/gdrive")


###############################################################
"""
IMPORTS
"""
import tensorflow as tf
import os
import pandas as pd
import numpy as np
import math
import pickle
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from bs4 import BeautifulSoup
import requests

#############################################################
"""
PATHS
"""
# cwd = os.getcwd()
dirname = os.path.dirname(__file__)
dataset_path = os.path.join(dirname, "datasets\\")
close_price_path = os.path.join(dirname, "close_prices\\")
models_path = os.path.join(dirname, "trainedModels\\")

# directory = "datasets\\"
# path = os.path.join(cwd, directory)
# dataset_path = path
# close_price_path = os.path.join(cwd, "close_prices\\")
# models_path = os.path.join(cwd, "trainedModels\\")
# dataset_path = '/content/gdrive/My Drive/datasets/'
# dataset_path = "C:\\Users\\knvga\\Desktop\\Projects\\TradeStation\\datasets\\"
# close_price_path = "C:\\Users\\knvga\\Desktop\\Projects\\TradeStation\\close_prices\\"
# close_price_path = '/content/gdrive/My Drive/close_prices/'
# models_path = "..\\trainedModels\\"

###########################################################


def extract_dataset_dic():
    files = {}
    for filename in os.listdir(dataset_path):
        files[filename.split(".")[0]] = pd.read_csv(dataset_path + filename)
    return files


# data cleaning
def data_cleaning():
    from datetime import datetime

    files = extract_dataset_dic()
    files_dic = {}
    for key, val in files.items():
        df = val
        df = df.loc[2850:]
        df = df.drop(
            columns=["Symbol", "Prev Close", "Last", "VWAP", "Volume", "Series"]
        )

        df.Date = pd.to_datetime(df.Date)
        first_date = "01-06-2011"
        df = df.assign(def_date=first_date)
        df.def_date = pd.to_datetime(df.def_date)
        df["Days"] = (df["Date"] - df["def_date"]).dt.days
        df = df.drop(columns=["Date", "def_date"])
        files_dic[key] = df
    return files_dic


def retrain_model():
    files_dic = data_cleaning()
    for key in files_dic.keys():
        data = pd.read_csv(f"{close_price_path + key}.csv")
        dataset = data.values
        training_data_len = math.ceil(len(dataset) * 0.75)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0:training_data_len, :]

        x_train = []
        y_train = []
        for i in range(30, len(train_data)):
            x_train.append(train_data[i - 30 : i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = Sequential()
        model.add(
            LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1))
        )
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=25))
        model.add(Dense(units=1))

        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(x_train, y_train, batch_size=50, epochs=50)

        # filename = f"{key}.pb"
        filepath = models_path + key
        tf.keras.models.save_model(
            model,
            filepath,
            overwrite=True,
            include_optimizer=True,
            save_format="h5",
            signatures=None,
            options=None,
            save_traces=True,
        )


def predict_price():
    # global scaler
    pred_price_dic = {}
    files_dic = data_cleaning()
    for key in files_dic.keys():
        # Create a new dataframe
        new_df = pd.read_csv(f"{close_price_path + key}.csv")

        dataset = new_df["Close"].values
        dataset = dataset.reshape(-1, 1)

        # #Scale the all of the data to be values between 0 and 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(dataset)
        # Get teh last 30 day closing price
        last_30_days = dataset[-30:]
        # Scale the data to be values between 0 and 1
        last_30_days_scaled = scaler.transform(last_30_days)
        # Create an empty list
        X_test = []
        # Append teh past 1 days
        X_test.append(last_30_days_scaled)
        # Convert the X_test data set to a numpy array
        X_test = np.array(X_test)
        # Reshape the data
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # Get the predicted scaled price
        filename = key
        model_path = models_path + filename

        loaded_model = tf.keras.models.load_model(model_path)

        # loaded_model = pickle.load(open(models_path + filename, "rb"))
        pred_price = loaded_model.predict(X_test)

        # undo the scaling
        pred_price = scaler.inverse_transform(pred_price)
        # print(key + '=' + str(pred_price))
        pred_price_dic[key] = pred_price
    return pred_price_dic
    # pred for next day


"""automatic obtaing dataset for everyday"""


def extract_daily_close_price():
    dic = {}
    files_dic = data_cleaning()
    for key in files_dic.keys():
        url = f"https://finance.yahoo.com/quote/{key}.NS/history?p={key}.NS"
        page = requests.get(url, headers={"User-Agent": "Custom"})
        soup = BeautifulSoup(page.text, "html.parser")
        price = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
        price = price.replace(",", "")
        price = float(price)
        dic[key] = price
    return dic


def update_dataset():
    prices_dic = extract_daily_close_price()
    files_dic = data_cleaning()
    for key in files_dic.keys():
        new_df = pd.read_csv(f"{close_price_path + key}.csv")
        price = prices_dic.get(key)
        # price = price.replace(",", "")
        qwe = pd.DataFrame([[price]], columns=["Close"])
        new_df = new_df.append(qwe, ignore_index=True)
        new_df.to_csv(f"{close_price_path+key}.csv", index=False)


"""profit percent

"""


def percent_change_dic():
    profit_dic = {}

    prices_dic = extract_daily_close_price()
    predictions = predict_price()

    for key in predictions.keys():
        true_price = prices_dic.get(key)  # true=yesterday price
        pred_price = predictions.get(key)

        percent_change = (pred_price - true_price) * 100 / true_price
        profit_dic[key] = percent_change
    return profit_dic


# retrain_model()
# prof = percent_change_dic()
# print(prof)
