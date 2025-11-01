import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib
from feature_engineering import extract_time_features



data = pd.read_excel("sensor_data.xlsx")


X = data.drop(columns=["RH_ERROR(Target)"])  
y = data["RH_ERROR(Target)"]


x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=101
)


pipeline = Pipeline([
    ("time_features", FunctionTransformer(extract_time_features)),
    ("model", XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    ))
])


pipeline.fit(x_train, y_train)


joblib.dump(pipeline, "sensor_model.pkl")