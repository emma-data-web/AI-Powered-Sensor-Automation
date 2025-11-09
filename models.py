
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from db import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    DHT_TEMP_C = Column(Float)
    DHT_RH = Column(Float)
    BME_TEMP_C = Column(Float)
    BME_RH = Column(Float)
    Pressure_hPa = Column(Float)
    RH_ERROR_pred = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
