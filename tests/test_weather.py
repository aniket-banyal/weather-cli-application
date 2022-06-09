import unittest
from datetime import datetime, timedelta

import weather
from weather import (get_cities_from_name, get_forecast_for_date,
                     get_lat_long_from_city)


class TestWeather(unittest.TestCase):

    def test_get_cities_from_name(self):
        city = 'chandigarh'
        cities = get_cities_from_name(city)
        self.assertIsInstance(cities, list)
        self.assertIn('name', cities[0])

    def test_get_lat_long_from_city(self):
        city = 'chandigarh'
        data = get_lat_long_from_city(city)
        self.assertIsInstance(data, tuple)
        self.assertTrue(len(data), 2)

    def test_get_forecast_for_date(self):
        date = datetime.now().date()
        forecast = get_forecast_for_date(lat=30, lon=30, date=date)

        self.assertIsInstance(forecast, dict)
        for field in weather.forecast_fields:
            self.assertIn(field, forecast)

    def test_get_forecast_for_date_returns_empty_dict_for_invalid_date(self):
        dates = [datetime.now().date() + timedelta(days=20), datetime.now().date() - timedelta(days=1)]

        for date in dates:
            forecast = get_forecast_for_date(lat=30, lon=30, date=date)
            self.assertIsInstance(forecast, dict)
            self.assertFalse(forecast)


if __name__ == '__main__':
    unittest.main()
