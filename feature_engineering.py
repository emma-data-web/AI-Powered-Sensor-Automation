import pandas as pd

def extract_time_features(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="coerce")

    data["hour"] = data["Timestamp"].dt.hour
    data["day"] = data["Timestamp"].dt.day
    data["month"] = data["Timestamp"].dt.month
    data["dayofweek"] = data["Timestamp"].dt.dayofweek
    data["is_weekend"] = data["dayofweek"].isin([5, 6]).astype(int)

    return data.drop(columns=["Timestamp"])