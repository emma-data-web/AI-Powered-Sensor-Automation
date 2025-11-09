
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib

from database import database, metadata
from models import SensorReading
from utils import save_reading


pipeline = joblib.load("sensor_model.pkl")


app = FastAPI(title="IoT Sensor Prediction API")


@app.on_event("startup")
async def startup():
    await database.connect()
    
    await database.execute(f"CREATE TABLE IF NOT EXISTS sensor_readings (id SERIAL PRIMARY KEY)")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()
        df = pd.DataFrame([data])
        prediction = pipeline.predict(df)[0]

        await save_reading(data, float(prediction))

        return {
            "status": "success",
            "received_data": data,
            "prediction": float(prediction),
            "message": "Prediction completed and saved, jeff and agnes let me rest."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Dashboard
@app.get("/readings", response_class=HTMLResponse)
async def get_readings():
    try:
        query = SensorReading.select().order_by(SensorReading.c.id.desc()).limit(50)
        readings = await database.fetch_all(query)

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
                <td>{r['id']}</td>
                <td>{r['DHT_TEMP_C']}</td>
                <td>{r['DHT_RH']}</td>
                <td>{r['BME_TEMP_C']}</td>
                <td>{r['BME_RH']}</td>
                <td>{r['Pressure_hPa']}</td>
                <td>{r['RH_ERROR_pred']}</td>
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
