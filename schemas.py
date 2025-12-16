
from pydantic import BaseModel
from datetime import datetime

class SensorReadingOut(BaseModel):
    
    id: int
    DHT_TEMP_C: float
    DHT_RH: float
    BME_TEMP_C: float
    BME_RH: float
    Pressure_hPa: float
    RH_ERROR_pred: float
    created_at: datetime 

    class Config:
        
        from_attributes = True