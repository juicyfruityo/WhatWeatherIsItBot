import requests
import json


class WeatherManager:
    def __init__(self):
        self.token = 'c96e8a61e1996f41d122a69312593c11'

    def __get_weather_now(self, city):
        token = self.token
        params = {'q': city, 'appid': token,
                  'lang': 'ru', 'units': 'metric'}
        weather_result = requests.get('https://api.openweathermap.org/data/2.5/weather',
                                      params=params)
        return weather_result

    def __convert_result(self, weather_result):
        temp = weather_result['main']['temp']
        descr = weather_result['weather'][0]['description']
        feels_like = weather_result['main']['feels_like']
        pressure = round(float(weather_result['main']['pressure']) / 1.333, 1)
        humidity = weather_result['main']['humidity']
        wind = weather_result['wind']['speed']

        return {'temp': temp, 'descr': descr, 'feels_like': feels_like,
                'pressure': pressure, 'humidity': humidity, 'wind': wind}

    def get_weather(self, city, when='now'):
        if when == 'now':
            weather_result = self.__get_weather_now(city)
        else:
            return -1, 'broken parameters'

        weather_result = json.loads(weather_result.text)

        result_code = int(weather_result['cod'])
        if result_code != 200:
            return result_code, weather_result['message']

        try:
            weather_result = self.__convert_result(weather_result)
        except Exception as e:
            return -1, "can't parse weather, " + str(e)

        return result_code, weather_result