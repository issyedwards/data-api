# pylint: disable=missing-module-docstring

import sys
from datetime import datetime, timedelta
import requests
import pandas as pd

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    '''Look for a given city. If multiple options are returned, have the user choose between them.
       Return one city (or None)
    '''
    url = f"{BASE_URI}/geo/1.0/direct?q={query}&limit=5"
    response = requests.get(url).json()
    if len(response) > 1:
        for i, value in enumerate(response):
            print(f"{i+1}. {value['name']},{value['country']}")
        print("Multiple matches found, which city did you mean?")
        idx = input()
        return response[int(idx)-1]
    if len(response) == 1:
        return response[0]
    return None

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    if isinstance(lat, float) and isinstance(lon, float):
        url = f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}&units=metric"
        response = requests.get(url).json()
        response = response["list"]
        five_day_forecast = []
        day = datetime.now() + timedelta(days=1)
        for entry in response:
            if entry.get("dt_txt").startswith(day.strftime("%Y-%m-%d")):
                five_day_forecast.append(entry)
                day = day + timedelta(days=1)
        dict_list = []
        for entry in five_day_forecast:
            weather_di = {}
            dt_txt = pd.to_datetime(
                entry.get("dt_txt"), format="%Y-%m-%d %H:%M:%S"
                ).strftime("%Y-%m-%d")
            weather_di['date'] = dt_txt
            weather_di['temp'] = str(entry["main"]["temp"])
            weather_di['weather'] = entry['weather'][0]['main']
            dict_list.append(weather_di)
            print(f"{weather_di['date']}: {weather_di['weather']} {weather_di['temp']} °C")
        return dict_list
    return None

def main():
    '''Ask user for a city and display weather forecast'''
    city = None
    while city is None:
        query = input("City?\n> ")
        city = search_city(query)
    weather_forecast(city['lat'], city['lon'])

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
