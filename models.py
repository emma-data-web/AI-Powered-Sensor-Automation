
from sqlalchemy import Table, Column, Integer, Float, DateTime
from datetime import datetime
from database import metadata

SensorReading = Table(
    "sensor_readings",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("DHT_TEMP_C", Float),
    Column("DHT_RH", Float),
    Column("BME_TEMP_C", Float),
    Column("BME_RH", Float),
    Column("Pressure_hPa", Float),
    Column("RH_ERROR_pred", Float),
    Column("created_at", DateTime, default=datetime.utcnow)
)
