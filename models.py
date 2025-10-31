from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    DHT_TEMP_C = Column(Float)
    DHT_RH = Column(Float)
    BME_TEMP_C = Column(Float)
    BME_RH = Column(Float)
    Pressure_hPa = Column(Float)
    RH_ERROR_pred = Column(Float)
