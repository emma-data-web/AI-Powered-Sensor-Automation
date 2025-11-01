from sqlalchemy.orm import Session
from models import SensorReading

def save_reading(db: Session, data: dict, prediction: float):
    reading = SensorReading(
        DHT_TEMP_C=data.get("DHT_TEMP_C"),
        DHT_RH=data.get("DHT_RH"),
        BME_TEMP_C=data.get("BME_TEMP_C"),
        BME_RH=data.get("BME_RH"),
        Pressure_hPa=data.get("Pressure_hPa"),
        RH_ERROR_pred=prediction
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

