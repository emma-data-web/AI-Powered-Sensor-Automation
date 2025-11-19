
from models import SensorReading
from db import SessionLocal

def save_reading(data: dict, prediction: float):
    
    db = SessionLocal()
    try:
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
        return reading.id  
    finally:
        db.close()

# incase of a rerun, use a live database