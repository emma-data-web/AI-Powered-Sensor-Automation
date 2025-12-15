import joblib
import pandas as pd

pipeline = joblib.load("sensor_model.pkl")

sample_data = {
    "DHT_TEMP_C": 25.2,
    "DHT_RH": 40.5,
    "BME_TEMP_C": 25.0,
    "BME_RH": 41.0,
    "Pressure_hPa": 1012.3
}

df = pd.DataFrame([sample_data])
print(pipeline.predict(df))
