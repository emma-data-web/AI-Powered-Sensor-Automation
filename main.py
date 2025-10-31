from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import joblib
from datetime import datetime

from .database import Base, engine, SessionLocal
from .models import SensorReading
from .utils import save_reading


Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Sensor Prediction API")


pipeline = joblib.load("sensor_model.pkl")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):
    try:

        data = await request.json()

        
        if "Timestamp" not in data:
            data["Timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame([data])

        
        prediction = pipeline.predict(df)[0]

        # Saving  to DB
        save_reading(db, data, float(prediction))

        return {
            "status": "success",
            "prediction": float(prediction),
            "message": "Prediction completed and logged successfully."
    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
