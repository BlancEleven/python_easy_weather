import datetime
import os
import sys
import unittest
sys.path.append(os.pardir)
import weather

class TestWeather(unittest.TestCase):

	def test_current(self):
		result = weather.current_conditions("04730", "imperial")
		self.assertEquals(len(result),1)
		self.assertEquals(len(result['descriptions']), 2)


	def test_wind_direction(self):
		self.assertEquals(weather.wind_direction(0), 'n')
		self.assertEquals(weather.wind_direction(15), 'ne')
		self.assertEquals(weather.wind_direction(90), 'e')
		self.assertEquals(weather.wind_direction(150), 'se')
		self.assertEquals(weather.wind_direction(180), 's')
		self.assertEquals(weather.wind_direction(195), 'sw')
		self.assertEquals(weather.wind_direction(270), 'w')
		self.assertEquals(weather.wind_direction(350), 'nw')


	def test_five_day(self):
		today = datetime.date.weekday(datetime.date.today())
		days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
		forecast = weather.five_day("04730", "metric")
		self.assertEquals(len(forecast), 5)
		self.assertEquals(list(forecast.items())[0][0], days[today])
		self.assertEquals(list(forecast.items())[4][0], days[today + 4])


if __name__ == '__main__':
	unittest.main() 