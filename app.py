from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from typing import Optional, Dict, List, Any
import uvicorn
from ghaim_ml import predictor

app = FastAPI(
    title="Ghaim UAE Weather API",
    description="API for UAE weather prediction and place recommendations",
    version="1.0.0"
)

class WeatherRequest(BaseModel):
    emirate: str
    date: Optional[str] = None
    

class WeatherResponse(BaseModel):
    emirate: str
    date: date
    weather: str
    recommendations: Dict[str, List[str]]

@app.get("/")
async def root():
    """Welcome endpoint with basic information about the API."""
    return {
        "message": "Welcome to the Ghaim UAE Weather API",
        "description": "Get weather predictions and place recommendations for UAE emirates",
    }

@app.get("/emirates", response_model=List[str])
async def get_emirates():
    """Get a list of all available UAE emirates in the system."""
    try:
        available_emirates = list(predictor.emirate_encoder.classes_)
        return available_emirates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emirates: {str(e)}")

#Create a new endpoint to get all 3 weather conditions Sunny, Rainy, Cloudy
@app.get("/weather_conditions", response_model=Dict[str, List[str]])
async def get_weather_conditions():
    try:
        weather_conditions = predictor.weather_encoder.classes_
        return {"weather_conditions": weather_conditions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve weather conditions: {str(e)}")
    
@app.post("/weather", response_model=WeatherResponse)
async def predict_weather(request: WeatherRequest):
    """
    Get weather prediction and place recommendations using a JSON request body.
    
    If no date is provided, today's weather will be predicted.
    """
    try:
        print(f"Received request: {request.json()}")
        # Validate emirate
        available_emirates = list(predictor.emirate_encoder.classes_)
        emirate = request.emirate
        # emirate = request.emirate.lower()
        if emirate not in available_emirates:
            raise HTTPException(status_code=400, detail=f"Invalid emirate. Available options: {available_emirates}")
        
        # Use today's date if none provided
        prediction_date = request.date
        
        if request.date=="today":
            prediction_date = datetime.today().date()
        elif request.date=="tomorrow":
            prediction_date = datetime.today().date() + timedelta(days=1)
        elif request.date==None:
            prediction_date = datetime.today().date()

        # Get prediction
        weather, recommendations = predictor.get_weather_and_place(emirate, prediction_date)
        
        return {
            "emirate": emirate,
            "date": prediction_date,
            "weather": weather,
            "recommendations": recommendations
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)