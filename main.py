from config.classes import *
from config.functions import *


def main():
    hh_api_obj = HeadHunterAPI()
    sj_api_obj = SuperJobAPI()
    # working_file = None
    # user_query = input("Введите ваш запрос: ")
    # print("Platforms:\n1. HeadHunter\n2. SuperJob")
    # user_select = input("Select platform (1 or 2): ")
    # if user_select == 1:
    #     hh_api_obj.get_vacancies(user_query)
    #     working_file = HHJSONFILE
    # elif user_select == 2:
    #     sj_api_obj.get_vacancies(user_query)
    #     working_file = SJJSONFILE
    # else:
    # #     print("Необходимо ввести цифру (номер платформы)")
    # sj_api_obj.get_vacancies('python')
    # hh_api_obj.get_vacancies('python')
    #
    # vacancy = Vacancy(12222222, "Вакансия через код", "1000 9000 руб", "https://pythonworld.ru",
    #                   "Самаяч тоапва яс варцнук фывл рофцуфрыовы вфт")

    vacancy = input_vacancy_info()
    vacancy.add_user_vacancy_to_json(HHJSONFILE)

if __name__ == '__main__':
    main()
