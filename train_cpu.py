import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib


data = pd.read_csv("real_sensor.csv")

x = data.drop("RH_ERROR(Target)", axis=1)
y = data["RH_ERROR(Target)"]


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=101)


model = XGBRegressor(tree_method='hist')


model.fit(x_train, y_train)


joblib.dump(model, "sensor_model_cpu.pkl")