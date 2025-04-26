from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from typing import Optional, Dict, List, Any, Union
import re
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
    
class AssistantQuery(BaseModel):
    query: str
    want_recommendations: Optional[bool] = False

class AssistantResponse(BaseModel):
    response_text: str
    parsed_emirate: Optional[str] = None
    parsed_date: Optional[date] = None
    weather: Optional[str] = None
    recommendations: Optional[Dict[str, List[str]]] = None
    success: bool
    error_message: Optional[str] = None

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

# New Ghaim Assistant API
@app.post("/assistant", response_model=AssistantResponse)
async def query_assistant(query_data: AssistantQuery):
    """
    Query the Ghaim Weather Assistant with natural language.
    
    This endpoint parses natural language queries about UAE weather and provides
    weather predictions and optionally place recommendations.
    
    Example query: "What's the weather in Dubai tomorrow?"
    """
    try:
        query = query_data.query.lower()
        want_recommendations = query_data.want_recommendations
        
        # Initialize response
        response = {
            "response_text": "",
            "parsed_emirate": None,
            "parsed_date": None,
            "weather": None,
            "recommendations": None,
            "success": False,
            "error_message": None
        }
        
        # Get available emirates
        available_emirates = list(predictor.emirate_encoder.classes_)
        
        # Parse query for emirate
        emirate = next((e for e in available_emirates if e.lower() in query), None)
        if not emirate:
            response["response_text"] = "Please mention a valid UAE emirate."
            response["error_message"] = "No valid emirate found in query"
            return response
        
        # Parse query for date
        today = datetime.today().date()
        if 'today' in query:
            date = today
        elif 'tomorrow' in query:
            date = today + timedelta(days=1)
        else:
            date_match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', query)
            if date_match:
                y, m, d = map(int, date_match.groups())
                date = datetime(y, m, d).date()
            else:
                response["response_text"] = "Please specify a date like 'today', 'tomorrow', or a full date (YYYY-MM-DD)."
                response["parsed_emirate"] = emirate
                response["error_message"] = "No valid date found in query"
                return response
        
        # Get weather prediction
        weather, recommendations = predictor.get_weather_and_place(emirate, date)
        
        # Build response
        response["response_text"] = f"The weather in {emirate.title()} on {date.strftime('%A, %B %d')} is expected to be {weather}."
        response["parsed_emirate"] = emirate
        response["parsed_date"] = date
        response["weather"] = weather
        response["success"] = True
        
        # Add recommendations if requested
        if want_recommendations:
            response["recommendations"] = recommendations
            recommendations_text = "\n\nRecommended places to visit:\n"
            for category, places in recommendations.items():
                if places:
                    recommendations_text += f"\n{category.title()} options include: "
                    recommendations_text += ", ".join(places[:3])
            
            response["response_text"] += recommendations_text
        
        return response
    
    except Exception as e:
        return {
            "response_text": "Sorry, something went wrong while processing your query.",
            "success": False,
            "error_message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)