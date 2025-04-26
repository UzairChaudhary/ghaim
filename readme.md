# Ghaim UAE Weather API

A FastAPI-based REST API for predicting weather in UAE emirates and recommending places to visit based on weather conditions.

## Overview

The Ghaim UAE Weather API provides a web interface to the "Ghaim" weather prediction and recommendation system. It supports natural language queries (similar to the voice assistant) and structured requests for weather data and place recommendations across all seven UAE emirates.

## Features

- Get weather predictions for any UAE emirate
- Receive place recommendations based on weather conditions
- Query the system using natural language through the assistant API
- List all available emirates
- Support for date options (today, tomorrow, or specific dates)

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/UzairChaudhary/ghaim.git
cd ghaim
```

2. Install the required packages:
```bash
pip install fastapi uvicorn pydantic
```


### Running the API

```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

### Base Information

- `GET /` - Welcome endpoint with API information
- `GET /emirates` - List all available UAE emirates
- `GET /weather` - Get weather prediction and recommendations
  - Request body:
    ```json
    {
      "emirate": "dubai",
      "date": "2023-07-15"  // Optional, defaults to today
    }
    ```

### Ghaim Assistant

- `POST /assistant` - Query the Ghaim Weather Assistant with natural language
  - Request body:
    ```json
    {
      "query": "What's the weather in Dubai tomorrow?",
      "want_recommendations": true  // Optional, defaults to false
    }
    ```

## Response Examples

### Weather Prediction Response

```json
{
  "emirate": "dubai",
  "date": "2023-07-15",
  "weather": "sunny",
  "recommendations": {
    "Outdoor Activities": ["Desert Safari", "Beach Club", "Garden Park"],
    "Indoor Venues": ["Dubai Mall", "Museum of the Future"],
    "Food & Drinks": ["Rooftop Restaurant", "Beachside Cafe"]
  }
}
```

### Assistant Response

```json
{
  "response_text": "The weather in Dubai on Saturday, July 15 is expected to be sunny.\n\nRecommended places to visit:\n\nOutdoor Activities options include: Desert Safari, Beach Club, Garden Park",
  "parsed_emirate": "dubai",
  "parsed_date": "2023-07-15",
  "weather": "sunny",
  "recommendations": {
    "Outdoor Activities": ["Desert Safari", "Beach Club", "Garden Park"],
    "Indoor Venues": ["Dubai Mall", "Museum of the Future"],
    "Food & Drinks": ["Rooftop Restaurant", "Beachside Cafe"]
  },
  "success": true,
  "error_message": null
}
```

## Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Error Handling

The API returns appropriate HTTP status codes:

- `400` - Bad Request (invalid emirate or date format)
- `500` - Internal Server Error (prediction or processing failure)

Error responses include a detail message explaining the issue.

