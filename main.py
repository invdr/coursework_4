from config.classes import *


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
    #     print("Необходимо ввести цифру (номер платформы)")

    sj_api_obj.get_vacancies('python')
    hh_api_obj.get_vacancies('python')


if __name__ == '__main__':
    main()
