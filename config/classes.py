import json
import os
from abc import ABC, abstractmethod

import requests

HHJSONFILE = 'config/hh_vacancies.json'
SJJSONFILE = 'config/sj_vacancies.json'


class APIVacancy(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, *args) -> None:
        pass

    @staticmethod
    def check_file(json_file) -> None:
        if not os.path.exists(json_file):
            raise FileNotFoundError("JSON файл не найден")


class JSONSaver:
    """Класс для сохранения вакансий со всех платформ в JSON формате"""

    @staticmethod
    def add_to_json(json_file, new_vacancies: list) -> None:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            json_data.extend(new_vacancies)

            # открываем файл для записи добавленных вакансий с каждой
            # страницы в список "items"
            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, ensure_ascii=False, indent=2)


class Vacancy(JSONSaver):
    """
    Класс для работы с вакансиями
    """

    def __init__(self, vacancy_id, profession, salary, url, description):

        if self.__check_values(vacancy_id, profession, salary, url, description):
            self.vacancy_id = vacancy_id
            self.profession = profession
            self.salary = salary
            self.vacancy_url = url
            self.description = description

    @classmethod
    def __check_values(cls, vacancy_id: int, profession: str, salary: dict | str, url: str, description: str) -> True:

        if not isinstance(vacancy_id, int):
            raise TypeError("ID Вакансии должен состоять из цифр")
        elif not len(str(vacancy_id)) == 8:
            raise ValueError("Длина ID вакансии должно быть равным 8 (восьми)")
        elif not len(profession) >= 10:
            raise TypeError("Наименование вакансии должно состоять из минимум 10 символов.")
        elif isinstance(salary, dict):
            if not salary["from"] or not salary["to"] or not salary["currency"]:
                raise KeyError("Не указано значение зарплаты ОТ, ДО или ВАЛЮТА")
        elif isinstance(salary, str):
            salary_split = salary.split()
            if len(salary_split) != 3:
                raise "Зарплата ОТ, ДО и ВАЛЮТА должны быть разделены пробелами (всего два пробела)"
            elif not int(salary_split[1]) >= int(salary_split[0]):
                raise "Зарплата ДО должна быть больше или равна зарплате ОТ"
            elif len(salary_split[2]) != 3:
                raise "Наименование валюты должно состоять из 3 букв"

        elif not url.startswith("https://"):
            raise "Ссылка должна начинаться с https://"
        elif not url.endswith(".ru"):
            raise "Ссылка должна заканчиваться на .ru"
        elif not len(description) >= 20:
            raise TypeError("Описание должно состоять минимум из 20 символов")

        return True

    @staticmethod
    def __get_user_salary(salary: str) -> dict:
        """Получает зарплата в виде "от-до"."""
        salary_list = salary.split()
        salary_dict = {
            "from": salary_list[0],
            "to": salary_list[1],
            "currency": salary_list[2].upper(),
        }
        return salary_dict

    def add_user_vacancy_to_json(self, json_file):
        vacancy = [{"id": self.vacancy_id,
                    "profession": self.profession,
                    "salary": self.salary if isinstance(self.salary, dict) else self.__get_user_salary(self.salary),
                    "vacancy_url": self.vacancy_url,
                    "description": self.description,
                    }]
        # используем метод класса JSONSaver для сохранения вакансии в рабочий JSON файл
        self.add_to_json(json_file, vacancy)

    @staticmethod
    def delete_vacancy(json_file, id_vacancy=None) -> None:
        with open(json_file, 'r', encoding='utf-8') as f:
            vacancies_list = json.load(f)
            if isinstance(id_vacancy, int):
                for index, vacancy in enumerate(vacancies_list):
                    if vacancy["id"] == id_vacancy:
                        vacancies_list.pop(index)
                        break
                else:
                    print("Такого индекса нет")
            else:
                vacancies_list.pop(-1)
            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(vacancies_list, outfile, ensure_ascii=False, indent=2)

    # def __gt__(self, other):
    #     """Сравнивает экземпляры класса по атрибуту salary"""
    #     return int(self.salary) > int(other.salary)
    #
    # def __ge__(self, other):
    #     """Сравнивает экземпляры класса по атрибуту subscriber_count."""
    #     return int(self.salary) >= int(other.salary)
    #
    # def __lt__(self, other):
    #     """Сравнивает экземпляры класса по атрибуту subscriber_count."""
    #     return int(self.salary) < int(other.salary)
    #
    # def __le__(self, other):
    #     """Сравнивает экземпляры класса по атрибуту subscriber_count."""
    #     return int(self.salary) <= int(other.salary)
    #
    # def __eq__(self, other):
    #     """Сравнивает экземпляры класса по атрибуту subscriber_count."""
    #     return int(self.salary) == int(other.salary)


class HeadHunterAPI(APIVacancy, JSONSaver):
    """Класс для работы с вакансиями сайта HH.ru посредством API."""

    def get_vacancies(self, query: str, json_file=HHJSONFILE) -> None:
        """По запросу пользователя добавляем найденные вакансии в JSON файл по шаблону."""
        # проверяем наличие необходимо JSON файла-шаблона
        self.check_file(json_file)

        # проходим в цикле по страницам результата запроса (100 записей на 1 страницу)
        for page in range(0, 1):
            new_data = json.loads(self.__get_page(query, page))

            # проверка на 2000 записей при 100 записях на 1 странице
            # если кол-во страниц результата запроса равно значению "page"
            # выходим из цикла
            if new_data['pages'] == page:
                break

            # список для форматированных вакансий
            formatted_vacancies = []
            for vacancy in new_data['items']:
                vacancy_info = {
                    "id": int(vacancy["id"]),
                    "profession": vacancy["name"],
                    # получаем зп, если есть, если нет - "Не указана"
                    "salary": self.__get_hh_salary(vacancy),
                    "vacancy_url": vacancy["alternate_url"],
                    # получаем требования, если есть, если нет - "Не указаны"
                    "description": self.__get_hh_description(vacancy),

                }
                formatted_vacancies.append(vacancy_info)

            # вызываем статический метод класса для записи вакансий в файл
            self.add_to_json(json_file, formatted_vacancies)

    @staticmethod
    def __get_page(query: str, page: int) -> str:
        """Функция получает JSON данные по вакансиям с необходимой страницы для дальнейшей работы."""
        params = {
            'text': f'NAME:{query}',
            'page': page,
            'per_page': 50,
        }

        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()  # декодируем
        return data

    @staticmethod
    def __get_hh_salary(vacancy: dict) -> str | dict:
        """Функция для записи зарплаты в JSON по шаблону."""
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
    def __get_hh_description(vacancy: dict) -> str:
        """Функция для записи требований в JSON по шаблону."""
        if vacancy["snippet"]["requirement"]:
            return f'{vacancy["snippet"]["requirement"]}'
        return 'Не указаны'


class SuperJobAPI(APIVacancy, JSONSaver):
    """Класс для работы с вакансиями сайта superjob.ru посредством API."""
    __secret_key = ('v3.h.4094091.ae6fa90f20bc0d67b04ec1edf5dd02e4ab9c64c5'
                    '.d238f3c7e7e5fe32997d9b4d0a15ff6a4d699b75')

    def get_vacancies(self, query: str, json_file=SJJSONFILE) -> None:
        """По запросу пользователя добавляем найденные вакансии в JSON файл по шаблону."""
        # проверяем наличие необходимо JSON файла-шаблона
        self.check_file(json_file)

        # проходим в цикле по страницам результата запроса (100 записей на 1
        # страницу)
        for page in range(0, 1):
            new_data = json.loads(self.__get_page(query, page))

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
                    "description": vacancy["candidat"],
                }
                formatted_vacancies.append(vacancy_info)

            # открываем файл для добавления вакансий с каждой страницы запроса
            # объекту "json_data"
            self.add_to_json(json_file, formatted_vacancies)

    @staticmethod
    def __get_page(query: str, page: int) -> str:
        """Функция получает JSON данные по вакансиям с необходимой страницы для дальнейшей работы."""
        headers = {'Host': 'api.superjob.ru',
                   'X-Api-App-Id': SuperJobAPI.__secret_key, }
        params = {'keyword': query,
                  'page': page,
                  'count': 100}

        req = requests.get('https://api.superjob.ru/2.0/vacancies/',
                           headers=headers, params=params)
        data = req.content.decode()  # декодируем
        return data
