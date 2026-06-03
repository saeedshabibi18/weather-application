from flask import Flask, render_template, request
import requests
import os
 
app = Flask(__name__)
 
API_KEY = os.environ.get("WEATHER_API_KEY", "demo")
BASE_URL = "http://api.weatherapi.com/v1/current.json"
 
@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
 
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            try:
                params = {
                    "key": API_KEY,
                    "q": city,
                    "aqi": "no"
                }
                resp = requests.get(BASE_URL, params=params, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    weather = {
                        "city": data["location"]["name"],
                        "country": data["location"]["country"],
                        "temp": round(data["current"]["temp_c"]),
                        "feels_like": round(data["current"]["feelslike_c"]),
                        "humidity": data["current"]["humidity"],
                        "description": data["current"]["condition"]["text"],
                        "icon": "https:" + data["current"]["condition"]["icon"],
                        "wind": data["current"]["wind_kph"],
                        "visibility": data["current"]["vis_km"],
                        "pressure": data["current"]["pressure_mb"],
                    }
                elif resp.status_code == 400:
                    error = f"City '{city}' not found. Please check the name."
                elif resp.status_code == 403:
                    error = "Invalid API key. Please check your WEATHER_API_KEY."
                else:
                    error = f"API error: {resp.status_code}"
            except requests.exceptions.Timeout:
                error = "Request timed out. Please try again."
            except Exception as e:
                error = f"Something went wrong: {str(e)}"
        else:
            error = "Please enter a city name."
 
    return render_template("index.html", weather=weather, error=error)
 
@app.route("/health")
def health():
    return {"status": "ok", "service": "weather-cicd-app"}, 200
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
    