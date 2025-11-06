import pandas as pd
from xgboost import XGBRegressor



data = pd.read_csv("complied_logs.csv")


print(data.head())


