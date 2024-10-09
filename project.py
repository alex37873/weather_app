"""
Модуль для получения и отображения погоды в выбранном городе.
"""

from datetime import datetime
from typing import Dict, List

import requests
from prettytable import PrettyTable

URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=is_day&hourly=temperature_2m,relative_humidity_2m,apparent_temperature&timeformat=unixtime&timezone=Europe%2FMoscow&forecast_days=1"


class Coordinates:
    """
    Класс для хранения географических координат города.
    """

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude


CITIES = {
    "Дубна": Coordinates(latitude=56.736343, longitude=37.162177),
    "Москва": Coordinates(latitude=55.755864, longitude=37.617698),
    "Казань": Coordinates(longitude=55.796127, latitude=49.106414),
    "Санкт-Петербург": Coordinates(latitude=59.938784, longitude=30.314997),
}


def get_weather_data(coordinates: Coordinates) -> Dict:
    """
    Функция для получения данных о погоде по заданным координатам.
    """

    url = URL.format(latitude=coordinates.latitude, longitude=coordinates.longitude)
    response = requests.get(url=url, timeout=60)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Запрос не выполнен с кодом состояния {response.status_code}...")
        exit()


def unix_time_to_human_readable(unix_timestamp: float, time_only: bool = False) -> str:
    """
    Конвертирует временную метку UNIX в читаемый формат времени.
    """

    dt_object = datetime.fromtimestamp(timestamp=unix_timestamp)
    if time_only:
        return dt_object.strftime(format="%H:%M")
    else:
        return dt_object.strftime(format="%d.%m.%Y %H:%M:%S")


def get_current_date_time(data: Dict) -> str:
    """
    Возвращает текущую дату и время из полученных данных о погоде.
    """

    return f"({"День" if data["current"]["is_day"] else "Ночь"}) {unix_time_to_human_readable(unix_timestamp=data["current"]["time"])} {data["timezone_abbreviation"]}"


def get_current_time(data: Dict) -> str:
    """
    Возвращает текущее время из полученных данных о погоде.
    """

    return f"{unix_time_to_human_readable(unix_timestamp=data["current"]["time"], time_only=True)}"


def get_horly_time(data: Dict) -> List[str]:
    """
    Извлекает часовые значения времени из полученных данных о погоде.
    """

    return [
        unix_time_to_human_readable(unix_timestamp=time, time_only=True)
        for time in data["hourly"]["time"]
    ]


def get_hourly_temperature_2m(data: Dict) -> List[str]:
    """
    Извлекает часовые значения температуры на высоте 2 метра из полученных данных о погоде.
    """

    return [
        f"{temperature} {data["hourly_units"]["temperature_2m"]}"
        for temperature in data["hourly"]["temperature_2m"]
    ]


def get_hourly_relative_humidity_2m(data: Dict) -> List[str]:
    """
    Извлекает часовые значения относительной влажности на высоте 2 метра из полученных данных о погоде.
    """

    return [
        f"{relative_humidity} {data["hourly_units"]["relative_humidity_2m"]}"
        for relative_humidity in data["hourly"]["relative_humidity_2m"]
    ]


def get_hourly_apparent_temperature(data: Dict) -> List[str]:
    """
    Извлекает часовые значения кажущейся температуры из полученных данных о погоде.
    """

    return [
        f"{apparent_temperature} {
            data["hourly_units"]["apparent_temperature"]}"
        for apparent_temperature in data["hourly"]["apparent_temperature"]
    ]


def main() -> None:
    """
    Основная функция для взаимодействия с пользователем и отображения данных о погоде.
    """

    print("Выберите город:")
    for index, (city_name, _) in enumerate(CITIES.items()):
        print(f"{index + 1}) {city_name}")

    while True:
        try:
            selection = int(input())
            selected_city_coordinates = CITIES[list(CITIES.keys())[selection - 1]]
            break
        except IndexError:
            print("Неверный выбор...")
            continue

    weather_data = get_weather_data(coordinates=selected_city_coordinates)

    table = PrettyTable()

    table.add_column(
        fieldname="Время",
        column=get_horly_time(data=weather_data),
    )
    table.add_column(
        fieldname="Температура",
        column=get_hourly_temperature_2m(data=weather_data),
    )
    table.add_column(
        fieldname="Относительная влажность",
        column=get_hourly_relative_humidity_2m(data=weather_data),
    )
    table.add_column(
        fieldname="Кажущаяся температура",
        column=get_hourly_apparent_temperature(data=weather_data),
    )

    print()
    print(get_current_date_time(data=weather_data))
    print(table)


if __name__ == "__main__":
    main()
