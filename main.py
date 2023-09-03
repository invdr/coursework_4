from config.classes import *
from config.functions import *


def main():
    working_platform = get_platform()
    user_query = input('Введите поисковый запрос: ')
    working_platform.get_vacancies(user_query)
    get_user_move()


    # vacancy = Vacancy(12222222, "Вакансия через код", "1000 9000 руб", "https://pythonworld.ru",
    #                   "Самаяч тоапва яс варцнук фывл рофцуфрыовы вфт")
    #
    # vacancy2 = Vacancy(12222222, "Вакансия через код", "1000 9000 руб", "https://pythonworld.ru",
    #                    "Самаяч тоапва яс варцнук фывл рофцуфрыовы вфт")
    #
    # vacancy3 = Vacancy(33333333, "Вакансия через код", "1000 9000 руб", "https://pythonworld.ru",
    #                    "Самаяч тоапва яс варцнук фывл рофцуфрыовы вфт")
    #
    # Vacancy.show_vacancies()
    # alll = Vacancy.all_added_vacancies
    # for v in alll:
    #     print(v)
    # # vacancy.add_user_vacancy_to_json(HHJSONFILE)
    # # vacancy.delete_vacancy(HHJSONFILE)
    # # delete_vacancy_in_json(HHJSONFILE)
    # top_n = check_top_n()
    # print(top_n)
    # # show_vacancies(HHJSONFILE)


if __name__ == '__main__':
    main()
