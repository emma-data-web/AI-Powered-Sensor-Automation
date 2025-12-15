
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import pandas as pd
import joblib

from db import Base, engine, SessionLocal
from models import SensorReading
from utils import save_reading
from llm import summarize_recent_errors 


pipeline = joblib.load("sensor_model.pkl")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Sensor Prediction API")


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

        df = pd.DataFrame([data])

        prediction = pipeline.predict(df)[0]

        save_reading(data, float(prediction))  

        return {
            "status": "success",
            "received_data": data,
            "prediction": float(prediction),
            "message": "Prediction completed and saved."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Dashboard 
@app.get("/readings", response_class=HTMLResponse)
def get_readings(db: Session = Depends(get_db)):
    try:
        
        readings = db.query(SensorReading).order_by(SensorReading.id.desc()).limit(50).all()

        
        html = """
        <html>
        <head>
            <title>Sensor Dashboard</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body { font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Live Sensor Predictions</h1>
            <p>Auto-refreshing every 5 seconds...</p>
            <table>
                <tr>
                    <th>Created At</th>
                    <th>ID</th>
                    <th>DHT_TEMP_C</th>
                    <th>DHT_RH</th>
                    <th>BME_TEMP_C</th>
                    <th>BME_RH</th>
                    <th>Pressure_hPa</th>
                    <th>RH_ERROR_pred</th>
                </tr>
        """

        for r in readings:
            html += f"""
            <tr>
                <td>{r.created_at}</td>
                <td>{r.id}</td>
                <td>{r.DHT_TEMP_C}</td>
                <td>{r.DHT_RH}</td>
                <td>{r.BME_TEMP_C}</td>
                <td>{r.BME_RH}</td>
                <td>{r.Pressure_hPa}</td>
                <td>{r.RH_ERROR_pred}</td>
            </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """
        return HTMLResponse(content=html)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading readings: {str(e)}")




@app.get("/summary")
def get_error_summary(db: Session = Depends(get_db), limit: int = 5):
    
    try:
        
        readings = db.query(SensorReading).order_by(SensorReading.id.desc()).limit(limit).all()
        
        
        readings_list = [
            {"RH_ERROR_pred": r.RH_ERROR_pred} for r in readings
        ]
        
        
        summary_text = summarize_recent_errors (readings_list)
        
        return {
            "status": "success",
            "summary": summary_text,
            "num_readings": len(readings_list)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
