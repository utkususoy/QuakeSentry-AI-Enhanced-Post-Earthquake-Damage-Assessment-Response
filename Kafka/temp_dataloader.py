import pandas as pd
import pickle

def load_temp_data():
    # with open("C:\\Users\\utkus\\Desktop\\Tez\\WorkingEnvironment\\Kafka\\multiple_broker\\temp_data\\Xtest_dataset.pickle", mode='rb') as f:
    #     x_data = pickle.load(f)
    # with open("C:\\Users\\utkus\\Desktop\\Tez\\WorkingEnvironment\\Kafka\\multiple_broker\\temp_data\\ytest_dataset.pickle", mode='rb') as f:
    #     y_data = pickle.load(f)
    # return x_data

    df = pd.read_csv("maras_complete_dmg_part5.csv")
    #df = df[df["label"] != "none"]
    return df["Text"]