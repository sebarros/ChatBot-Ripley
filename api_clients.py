import requests


class WeatherAPIClient:

    GEO = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, city: str):

        geo = requests.get(self.GEO, params={
            "name": city,
            "count": 1,
            "language": "es"
        }).json()

        if "results" not in geo or not geo["results"]:
            return {"error": "city_not_found"}

        city_data = geo["results"][0]

        weather = requests.get(self.WEATHER, params={
            "latitude": city_data["latitude"],
            "longitude": city_data["longitude"],
            "current_weather": True
        }).json().get("current_weather", {})

        return {
            "city": city_data["name"],
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed")
        }


class ProductAPIClient:

    BASE = "https://fakestoreapi.com"

    def get_products(self):
        return requests.get(f"{self.BASE}/products").json()