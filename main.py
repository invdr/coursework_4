import pprint

from config.functions import *


def main():
    working_platform = get_platform()  #
    working_file = working_platform.get_working_file
    user_query = input('Введите поисковый запрос: ')
    working_platform.get_vacancies(user_query)
    user_interaction(working_file)


def add_vacancy_without_terminal():
    vacancy = Vacancy(11111111, "Python джуниор", "100000 200000 руб", "https://python.ru",
                      "Вакансия для джуниора. Требования: Python, SQL, Django 4")
    vacancy2 = Vacancy(11111112, "Python middle", "150000 200000 руб", "https://python.ru",
                       "Вакансия для middle. Требования: Python, SQL, Django 4")
    vacancy3 = Vacancy(11111113, "Python senior", "200000 250000 руб", "https://python.ru",
                       "Вакансия для Senior. Требования: Python, SQL, Django 4")

    json_file = vacancy.get_working_file  # получаем путь к json файлу
    # добавляем вакансии в json файл
    vacancy.add_user_vacancy_to_json(json_file)
    vacancy2.add_user_vacancy_to_json(json_file)
    vacancy3.add_user_vacancy_to_json(json_file)
    pprint.pp(vacancy.all_added_vacancies)

    # сравнение экземпляров по зарплате ОТ
    print()
    print(vacancy2 == vacancy)  # False
    print(vacancy == vacancy2)  # False
    print(vacancy2 > vacancy3)  # False
    print(vacancy3 > vacancy2)  # True
    print(vacancy < vacancy3)  # True
    print(vacancy3 < vacancy)  # False
    print(vacancy <= vacancy3)  # True
    print(vacancy3 >= vacancy)  # True
    print()

    # удаляем вакансию из json файла и сам экземпляр из списка
    vacancy.delete_vacancy(json_file)  # ---------- Вакансия и экземпляр из списка удалены ----------
    vacancy2.delete_vacancy(json_file)  # ---------- Вакансия и экземпляр из списка удалены ----------
    pprint.pp(vacancy.all_added_vacancies)


if __name__ == '__main__':
    add_vacancy_without_terminal()
