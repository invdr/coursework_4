import json
import os
from abc import ABC, abstractmethod

import requests

HHJSONFILE = 'config/hh_vacancies.json'
SJJSONFILE = 'config/sj_vacancies.json'


class APIVacancy(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, *args):
        pass

    @staticmethod
    def check_file(json_file):
        if not os.path.exists(json_file):
            raise FileNotFoundError("JSON файл не найден")


class JSONSaver:
    """Класс для сохранения вакансий со всех платформ в JSON формате"""
    @staticmethod
    def add_to_json(json_file, new_vacancies):
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            json_data.extend(new_vacancies)

            # открываем файл для записи добавленных вакансий с каждой
            # страницы в список "items"
            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, ensure_ascii=False, indent=2)


class HeadHunterAPI(APIVacancy, JSONSaver):
    """Класс для работы с API сайта HH.ru"""

    def get_vacancies(self, query, json_file=HHJSONFILE):
        """По запросу пользователя добавляем найденные вакансии в JSON файл по шаблону."""
        # проверяем наличие необходимо JSON файла-шаблона
        self.check_file(json_file)

        # проходим в цикле по страницам результата запроса (100 записей на 1 страницу)
        for page in range(0, 1):
            new_data = json.loads(self.get_page(query, page))

            # проверка на 2000 записей при 100 записях на 1 странице
            # если кол-во страниц результата запроса равно значению "page"
            # выходим из цикла
            if new_data['pages'] == page:
                break

            # список для форматированных вакансий
            formatted_vacancies = []
            for vacancy in new_data['items']:
                vacancy_info = {
                    "id": vacancy["id"],
                    "profession": vacancy["name"],
                    # получаем зп, если есть, если нет - "Не указана"
                    "salary": self.get_hh_salary(vacancy),
                    "vacancy_url": vacancy["alternate_url"],
                    # получаем требования, если есть, если нет - "Не указаны"
                    "snippet": self.get_hh_requirements(vacancy),

                }
                formatted_vacancies.append(vacancy_info)

            # вызываем статический метод класса для записи вакансий в файл
            self.add_to_json(json_file, formatted_vacancies)

    @staticmethod
    def get_page(query, page=0):
        params = {
            'text': f'NAME:{query}',
            'page': page,
            'per_page': 50,
        }

        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()  # декодируем
        return data

    @staticmethod
    def get_hh_salary(vacancy):
        """Функция для записи зп в json"""
        if vacancy["salary"]:
            salary_from = vacancy["salary"]["from"]
            salary_to = vacancy["salary"]["to"]
            currency = vacancy["salary"]["currency"]
        else:
            return 'Не указана'

        salary = {"from": salary_from,
                  "to": salary_to,
                  "currency": currency, }

        return salary

    @staticmethod
    def get_hh_requirements(vacancy):
        """Функция для записи требований в json"""
        if vacancy["snippet"]["requirement"]:
            return f'{vacancy["snippet"]["requirement"]}'
        return 'Не указаны'


class SuperJobAPI(APIVacancy, JSONSaver):
    """Класс для работы с API сайта superjob.ru"""
    __secret_key = ('v3.h.4094091.ae6fa90f20bc0d67b04ec1edf5dd02e4ab9c64c5'
                    '.d238f3c7e7e5fe32997d9b4d0a15ff6a4d699b75')

    def get_vacancies(self, query, json_file=SJJSONFILE):

        self.check_file(json_file)

        # проходим в цикле по страницам результата запроса (100 записей на 1
        # страницу)
        for page in range(0, 1):
            new_data = json.loads(self.get_page(query, page))

            # список для форматированных вакансий
            formatted_vacancies = []
            for vacancy in new_data['objects']:
                vacancy_info = {
                    "id": vacancy["id"],
                    "profession": vacancy["profession"],
                    "salary": {
                        "from": vacancy["payment_from"],
                        "to": vacancy["payment_to"],
                        "currency": vacancy["currency"].upper(),
                    },
                    "vacancy_url": vacancy["link"],
                    "snippet": vacancy["candidat"],
                }
                formatted_vacancies.append(vacancy_info)

            # открываем файл для добавления вакансий с каждой страницы запроса
            # объекту "json_data"
            self.add_to_json(json_file, formatted_vacancies)

    @staticmethod
    def get_page(query, page=0):
        headers = {'Host': 'api.superjob.ru',
                   'X-Api-App-Id': SuperJobAPI.__secret_key, }
        params = {'keyword': query,
                  'page': page,
                  'count': 100}

        req = requests.get('https://api.superjob.ru/2.0/vacancies/',
                           headers=headers, params=params)
        data = req.content.decode()  # декодируем
        return data


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, id, name, url, salary, description, something):
        self.__check_values(name, url, salary, description)
        self.id = id
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    @classmethod
    def __check_values(cls, name, url, salary, description):
        if not isinstance(name, str):
            raise 'Название вакансии должно быть строковым значением'

    def __gt__(self, other):
        """Сравнивает экземпляры класса по атрибуту subscriber_count."""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Сравнивает экземпляры класса по атрибуту subscriber_count."""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """Сравнивает экземпляры класса по атрибуту subscriber_count."""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Сравнивает экземпляры класса по атрибуту subscriber_count."""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """Сравнивает экземпляры класса по атрибуту subscriber_count."""
        return int(self.subscriber_count) == int(other.subscriber_count)
