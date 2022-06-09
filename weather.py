import json
import urllib.request
from datetime import datetime

from helpers import get_formatted_date

OPEN_WEATHER_API_KEY = 'aa38ddb07728ac3c4b6bb0ce88fd3437'


def get_cities_from_name(city):
    city = urllib.parse.quote_plus(city)

    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={OPEN_WEATHER_API_KEY}'
    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        data = json.loads(data)
        return data


def get_lat_long_from_city(city):
    city = urllib.parse.quote_plus(city)
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={OPEN_WEATHER_API_KEY}'

    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        data = json.loads(data)
        city_data = data[0]

    return city_data.get('lat'), city_data.get('lon')


def __get_data_from_api(lat, lon):
    exclude_fields = ('current', 'minutely', 'hourly', 'alerts')
    exclude = ','.join(exclude_fields)

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={OPEN_WEATHER_API_KEY}'

    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        data = json.loads(data)
    return data.get('daily')


forecast_fields = ['humidity', 'pressure', 'temperature', 'wind speed', 'wind degree', 'uv index']


def __get_forecast_data(lat, lon):
    daily_forecasts = __get_data_from_api(lat, lon)

    data = {}
    for forecast in daily_forecasts:
        forecast_datetime = datetime.fromtimestamp(forecast.get('dt'))
        t = {}
        t['humidity'] = forecast.get('humidity')
        t['pressure'] = forecast.get('pressure')
        t['temperature'] = forecast.get('temp').get('day')
        t['wind speed'] = forecast.get('wind_speed')
        t['wind degree'] = forecast.get('wind_deg')
        t['uv index'] = forecast.get('uvi')
        data[forecast_datetime.date()] = t
    return data


def get_forecast_for_date(lat, lon, date):
    data = __get_forecast_data(lat, lon)

    forecast = data.get(date, {})
    if not forecast:
        dates = list(data.keys())
        start_date, end_date = dates[0], dates[-1]
        print(f'Can forecast only from {get_formatted_date(start_date)} to {get_formatted_date(end_date)}.')
    return forecast
