from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="templates")


# Route for the home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route for handling form submission
@app.post("/")
def get_weather(request: Request, city: str = Form(...)):
    # OpenWeatherMap API key and endpoint
    api_key = "f3f7c9db9ae85564e2a9e60c306f86cd"
    endpoint = "http://api.openweathermap.org/data/2.5/weather"

    # Make a request to the OpenWeatherMap API
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(endpoint, params=params)
    weather_data = response.json()

    # Extract relevant information from the API response
    temperature = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "city": city,
            "temperature": temperature,
            "wind_speed": wind_speed,
            "description": description,
        },
    )


if __name__ == "__main__":
    import uvicorn

    # Run the application using Uvicorn
    uvicorn.run(app)
