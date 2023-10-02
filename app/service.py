from pyowm import OWM

'''
Памятка
Дефолтный статус - w.detailed_status
Ветер - w.wind()
Влажность - w.humidity
Дождь - w.rain
Облачность - w.clouds
Температура в цельсиях - w.temperature('celsius')
'''

owm = OWM('eea9a437382f7456fddce945eb3fed33')
mgr = owm.weather_manager()


class CityWeather:
    def __init__(self, name):
        observation = mgr.weather_at_place(name)
        w = observation.weather
        self.name = observation.location.name
        self.status = w.detailed_status
        self.speed_wind = w.wind()['speed']
        self.humidity = w.humidity
        self.cloud = w.clouds
        self.temperature = w.temperature('celsius')['temp']
        self.temperature_feels_like = w.temperature('celsius')['feels_like']


class ForecastCity:
    def __init__(self, name):
        self.name = name
        # Ключи начинаются с двойки, так как под первым индексом находится неподходящее время, которое выдает API
        self.res = {k: {} for k in range(2, 9 + 1)}

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
    def del_city(name):
        for i in range(len(ContainerCities.container) - 1, 0 - 1, -1):
            if ContainerCities.container[i].name == name:
                ContainerCities.container.pop(i)

    @staticmethod
    def delete_all_cities():
        ContainerCities.container.clear()

    @staticmethod
    def add_all_cities(cities):
        for elem in cities:
            city = CityWeather(elem.city)
            ContainerCities.container.append(city)

    @staticmethod
    def del_and_get_all_cities(cities):
        ContainerCities.delete_all_cities()
        ContainerCities.add_all_cities(cities)
        return ContainerCities.container



