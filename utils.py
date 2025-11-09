
from models import SensorReading
from database import database

async def save_reading(data: dict, prediction: float):
    query = SensorReading.insert().values(
        DHT_TEMP_C=data.get("DHT_TEMP_C"),
        DHT_RH=data.get("DHT_RH"),
        BME_TEMP_C=data.get("BME_TEMP_C"),
        BME_RH=data.get("BME_RH"),
        Pressure_hPa=data.get("Pressure_hPa"),
        RH_ERROR_pred=prediction
    )
    record_id = await database.execute(query)
    return record_id
