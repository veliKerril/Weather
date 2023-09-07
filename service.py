from pyowm import OWM
from pyowm.utils import timestamps

cities = {
    'Moscow': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Saint-Petersburg': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Rostov-on-Don': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Yekaterinburg': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
}

# # Дефолтный статус
# print(w.detailed_status)
# # Ветер
# print(w.wind())
# # Влажность
# print(w.humidity)
# # Дождь
# print(w.rain)
# # Облачность
# print(w.clouds)
# # Температура в цельсиях
# print(w.temperature('celsius'))

owm = OWM('eea9a437382f7456fddce945eb3fed33')
mgr = owm.weather_manager()


class CityWeather:
    def __init__(self, name):
        observation = mgr.weather_at_place(name)
        w = observation.weather
        self.name = name
        self.status = w.detailed_status
        self.speed_wind = w.wind()['speed']
        self.humidity = w.humidity
        self.cloud = w.clouds
        self.temperature = w.temperature('celsius')['temp']
        self.temperature_feels_like = w.temperature('celsius')['feels_like']

    def return_all_info(self):
        return {
            'Дефолтный статус: ': self.status,
            'Скорость ветра: ': self.speed_wind['speed'],
            'Влажность: ': str(self.speed_wind) + '%',
            'Облачность: ': str(self.cloud) + '%',
            'Средняя температура в цельсиях: ': self.temperature,
            'Ощущение температуры: ': self.temperature_feels_like,
        }


class ForecastCity:
    def __init__(self, name):
        self.name = name
        self.res = {
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {}
        }

    def get_forecast(self):
        three_h_forecast = mgr.forecast_at_place(self.name, '3h').forecast
        count = 1
        for w in three_h_forecast:
            if count == 1:
                count += 1
                continue

            if count == 10:
                break

            self.res[count]['time'] = w.reference_time(timeformat='iso')[11:16]
            self.res[count]['status'] = w.detailed_status
            self.res[count]['speed_wind'] = w.wind()['speed']
            self.res[count]['humidity'] = w.humidity
            self.res[count]['cloud'] = w.clouds
            self.res[count]['temperature'] = w.temperature('celsius')['temp']
            self.res[count]['temperature_feels_like'] = w.temperature('celsius')['feels_like']

            count += 1

        return self.res


class ContainerCities:
    container = []

    @staticmethod
    def add_city(name):
        city = CityWeather(name)
        ContainerCities.container.append(city)

    @staticmethod
    def del_city(name):
        for i in range(len(ContainerCities.container) - 1, 0 - 1, -1):
            if ContainerCities.container[i].name == name:
                ContainerCities.container.pop(i)

    @staticmethod
    def get_all_cities():
        return ContainerCities.container


