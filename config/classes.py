import json
import os
from abc import ABC, abstractmethod

import requests


class APIVacancy(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""
    __slots__ = ()

    @abstractmethod
    def get_vacancies(self, *args) -> None:
        pass


class Saver(ABC):
    """Абстрактный класс для сохранения вакансий в файл."""

    @staticmethod
    @abstractmethod
    def add_vacancies(*args):
        pass

    @staticmethod
    def print_result(json_data):
        """Возвращает результат сбора вакансий."""
        if json_data:
            print_pos_result = '\n---------- Сохранено в файл ----------\n'
            return print_pos_result
        print_neg_result = '---------- Вакансии с таким запросом не найдены ----------\n'
        return print_neg_result

    @staticmethod
    def check_file(json_file) -> None:
        if not os.path.exists(json_file):
            raise FileNotFoundError("JSON файл с вакансиями не найден")


class JSONSaver(Saver):
    """Класс для сохранения вакансий в JSON формате."""
    __slots__ = ()
    working_file = 'config/vacancies.json'

    def __init__(self):
        # проверяем наличие необходимо JSON файла-шаблона
        if self.check_file(JSONSaver.working_file):
            self.__working_file = self.working_file

    @property
    def get_working_file(self):
        return self.working_file

    @staticmethod
    def add_vacancies(json_file, new_vacancies: list) -> None:
        """Метод добавления найденных вакансий по запросу в JSON файл"""
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            json_data.extend(new_vacancies)

            # открываем файл для записи добавленных вакансий с каждой
            # страницы в список "items"
            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, ensure_ascii=False, indent=2)
            print(Saver.print_result(json_data))


class Vacancy(JSONSaver):
    """Класс для работы с вакансиями."""
    __slots__ = ('vacancy_id', 'profession', 'salary', 'vacancy_url', 'description')
    all_added_vacancies = []

    def __init__(self, vacancy_id, profession, salary, vacancy_url, description):
        super().__init__()
        if self.__check_values(vacancy_id, profession, salary, vacancy_url, description):
            self.vacancy_id = vacancy_id
            self.profession = profession
            self.salary = salary
            self.vacancy_url = vacancy_url
            self.description = description

        self.all_added_vacancies.append(self)

    @classmethod
    def __check_values(cls, vacancy_id: int, profession: str, salary: dict | str, vacancy_url: str,
                       description: str) -> True:
        """Метод класса для возбуждения исключений при неверных входных данных."""
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
                raise "Зарплата и валюта должны быть разделены пробелами (всего два пробела)"
            elif not int(salary_split[1]) >= int(salary_split[0]):
                raise "Зарплата ДО должна быть больше или равна зарплате ОТ"
            elif len(salary_split[2]) != 3:
                raise "Наименование валюты должно состоять из 3 букв"
        elif not vacancy_url.startswith("https://"):
            raise "Ссылка должна начинаться с https://"
        elif not vacancy_url.endswith(".ru"):
            raise "Ссылка должна заканчиваться на .ru"
        elif not len(description) >= 20:
            raise TypeError("Описание должно состоять минимум из 20 символов")

        return True

    @staticmethod
    def __get_user_salary(salary: str) -> dict:
        """Получает зарплату в виде "от до валюта" и возвращает в виде словаря."""
        salary_list = salary.split()
        salary_dict = {
            "from": salary_list[0],
            "to": salary_list[1],
            "currency": salary_list[2].upper(),
        }
        return salary_dict

    def add_user_vacancy_to_json(self, json_file):
        """Метод для добавления пользовательской вакансии в JSON файл."""
        vacancy = [{"id": self.vacancy_id,
                    "profession": self.profession,
                    "salary": self.salary if isinstance(self.salary, dict) else self.__get_user_salary(self.salary),
                    "vacancy_url": self.vacancy_url,
                    "description": self.description,
                    }]
        # используем метод класса JSONSaver для сохранения вакансии в рабочий JSON файл
        self.add_vacancies(json_file, vacancy)

    def delete_vacancy(self, json_file) -> None:
        """Метод для удаления вакансии из JSON файла и списка экземпляров."""
        with open(json_file, 'r', encoding='utf-8') as f:
            vacancies_list = json.load(f)
            vacancies_list.pop()
            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(vacancies_list, outfile, ensure_ascii=False, indent=2)
        self.all_added_vacancies.pop()  # удаляем из списка экземпляров
        print("---------- Вакансия и экземпляр удалены ----------\n")

    @classmethod
    def show_vacancies(cls):
        """Показывает все добавленные вакансии."""
        for vac in cls.all_added_vacancies:
            vacancy_info = ('------------------\n'
                            f'ID вакансии: {vac.vacancy_id}\n'
                            f'Наименование вакансии: {vac.profession}\n'
                            f'Зарплата: \n'
                            f'\tОт: {vac.salary["from"]}\n'
                            f'\tДо: {vac.salary["to"]}\n'
                            f'\tВалюта: {vac.salary["currency"]}\n'
                            f'Ссылка: {vac.vacancy_url}\n'
                            f'Описание: {vac.description}')
            print(vacancy_info)

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

    def __str__(self):
        salary = self.__get_user_salary(self.salary)
        vacancy_info = ('------------------\n'
                        f'ID вакансии: {self.vacancy_id}\n'
                        f'Наименование вакансии: {self.profession}\n'
                        f'Зарплата: \n'
                        f'\tОт: {salary["from"]}\n'
                        f'\tДо: {salary["to"]}\n'
                        f'\tВалюта: {salary["currency"]}\n'
                        f'Ссылка: {self.vacancy_url}\n'
                        f'Описание: {self.description}')
        return vacancy_info

    def __repr__(self):
        return (f'{self.__class__.__name__}({self.vacancy_id=}, {self.profession=}, '
                f'{self.salary=}, {self.vacancy_url=}, {self.description=})')


class HeadHunterAPI(APIVacancy, JSONSaver):
    """Класс для работы с вакансиями сайта HH.ru посредством API."""
    __slots__ = ()

    def get_vacancies(self, query: str) -> None:
        """По запросу пользователя добавляем найденные вакансии в JSON файл по шаблону."""
        # ссылка на файл для работы
        working_file = self.get_working_file

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
            self.add_vacancies(working_file, formatted_vacancies)

    @staticmethod
    def __get_page(query: str, page: int) -> str:
        """Функция получает данные по вакансиям с необходимой страницы для дальнейшей работы."""
        params = {
            'text': f'NAME:{query}',
            'page': page,
            'per_page': 10,
        }

        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()  # декодируем
        return data

    @staticmethod
    def __get_hh_salary(vacancy: dict) -> str | dict:
        """Метод для записи зарплаты в JSON по шаблону."""
        if vacancy["salary"]:
            salary_from = vacancy["salary"]["from"]
            salary_to = vacancy["salary"]["to"]
            if vacancy["salary"]["currency"] == "RUR":
                currency = "RUB"
            else:
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
        return 'Не указано'


class SuperJobAPI(APIVacancy, JSONSaver):
    """Класс для работы с вакансиями сайта superjob.ru посредством API."""
    __slots__ = ()

    secret_key = os.getenv('sj_key')

    def get_vacancies(self, query: str) -> None:
        """По запросу пользователя добавляем найденные вакансии в JSON файл по шаблону."""
        # ссылка на файл для работы
        working_file = self.get_working_file

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

                    "salary": self.__get_sj_salary(vacancy),
                    "vacancy_url": vacancy["link"],
                    "description": vacancy["candidat"],
                }
                formatted_vacancies.append(vacancy_info)

            # открываем файл для добавления вакансий с каждой страницы запроса
            # объекту "json_data"
            self.add_vacancies(working_file, formatted_vacancies)

    @staticmethod
    def __get_page(query: str, page: int) -> str:
        """Функция получает JSON данные по вакансиям с необходимой страницы для дальнейшей работы."""
        headers = {'Host': 'api.superjob.ru',
                   'X-Api-App-Id': SuperJobAPI.secret_key, }
        params = {'keyword': query,
                  'page': page,
                  'count': 10}

        req = requests.get('https://api.superjob.ru/2.0/vacancies/',
                           headers=headers, params=params)
        data = req.content.decode()  # декодируем
        return data

    @staticmethod
    def __get_sj_salary(vacancy: dict) -> str | dict:
        """Метод для записи зарплаты в JSON по шаблону."""
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
        currency = vacancy["currency"].upper()

        if salary_from == 0 and salary_to == 0:
            return 'Не указана'

        salary = {"from": salary_from,
                  "to": salary_to,
                  "currency": currency, }

        return salary
