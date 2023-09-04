from config.classes import *
from config.functions import *


def main():
    working_platform = get_platform()
    working_file = working_platform.get_working_file
    user_query = input('Введите поисковый запрос: ')
    working_platform.get_vacancies(user_query)
    get_user_move(working_file)

if __name__ == '__main__':
    main()
