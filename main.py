from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import pandas as pd
import joblib
from datetime import datetime

from database import Base, engine, SessionLocal
from models import SensorReading
from utils import save_reading

# Load pipeline once
pipeline = joblib.load("sensor_model.pkl")

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Sensor Prediction API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- PREDICTION ENDPOINT ---------------------- #
@app.post("/predict")
async def predict(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()

        # Convert input to DataFrame
        df = pd.DataFrame([data])

        # Predict
        prediction = pipeline.predict(df)[0]

        # Save input and prediction to DB
        save_reading(db, data, float(prediction))

        return {
            "status": "success",
            "received_data": data,
            "prediction": float(prediction),
            "message": "Prediction completed and saved."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# ---------------------- DASHBOARD ENDPOINT ---------------------- #
@app.get("/readings", response_class=HTMLResponse)
def get_readings(db: Session = Depends(get_db)):
    readings = db.query(SensorReading).all()

    # Build the table
    html = """
    <html>
    <head>
        <title>Sensor Dashboard</title>
        <meta http-equiv="refresh" content="5"> <!-- Auto-refresh every 5s -->
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Live Sensor Predictions</h1>
        <p>Auto-refreshing every 5 seconds...</p>
        <table>
            <tr>
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
    return html
