import random
#класс для мониторинга погоды
class WeatherMonitor:
    def __init__(self):
        self.city = "Moscow" #в качестви проверки выбрана Москва

    def get_current_weather(self) -> dict: #функция получения текущией погоды
        conditions = ["Clear", "Cloudy", "Rainy", "Snowing"]
        return {
            "city": self.city,
            "temp": random.randint(-5, 25), #генерация рандомной температуры
            "condition": random.choice(conditions)
        }
