import json

from config.classes import *


def get_user_move(json_file):
    print("\nДоступные действия:\n"
          "1. Показать все собранные вакансии\n"  # show_vacancies(json_file, top_n=0)
          "2. Показать вакансию по ID\n"  # не реализовано
          "3. Показать топ N вакансий\n"  # show_vacancies(json_file, top_n=0)
          "4. Удалить вакансию из собранных по его ID\n"  # delete_vacancy_by_id(json_file)
          "5. Добавить вакансию в список")  # Vacancy.
    if Vacancy.all_added_vacancies:
        print("6. Показать добавленную вакансию\n"  # print(vacancy)
              "7. Удалить добавленную вакансию")  # delete_vacancy(self, json_file)
    if len(Vacancy.all_added_vacancies) > 1:
        print("8. Показать все добавленные вакансии\n")
    print("0. Выход")
    user_move = int(input("Выберите действие: "))
    while user_move != 0:
        if user_move == 1:
            show_vacancies(json_file)
            get_user_move(json_file)
        elif user_move == 2:
            pass
        elif user_move == 3:
            top_n = get_top_n()
            show_vacancies(json_file, top_n)
            get_user_move(json_file)
        elif user_move == 4:
            delete_vacancy_by_id(json_file)
            get_user_move(json_file)
        elif user_move == 5:
            vacancy = add_vacancy()
            vacancy.add_user_vacancy_to_json(json_file)
            get_user_move(json_file)
        # elif user_move == 6:
        #     last_added_vac = Vacancy.all_added_vacancies[-1]
        #     print(last_added_vac)
        # elif user_move == 7:
        #     last_added_vac = Vacancy.all_added_vacancies[-1]
        #     Vacancy.delete_vacancy(last_added_vac, json_file)
        else:
            print("Не то число")
            get_user_move(json_file)
    # return user_move


def get_platform():
    platforms = (HeadHunterAPI(), SuperJobAPI())
    print("Выберите платформу сбора вакансий: ")
    print("1. HeadHunter\n2. SuperJob\n")

    validated_platform = None
    validate = False
    while not validate:
        input_platform = input("Введите номер платформы: ")
        if not input_platform.isdigit():
            print("Введите число 1 для HH или 2 для SuperJob цифрами")
        elif not int(input_platform) in (1, 2):
            print("Введите число 1 для HH или 2 для SuperJob")
        else:
            validated_platform = int(input_platform)
            validate = True
    # создаем объект для работы с API
    if validated_platform == 1:
        return platforms[0]
    return platforms[1]


def get_working_file(platform) -> str:
    return platform.get_working_file


def show_vacancies(json_file, top_n=0) -> None:
    """
    Печатает вакансии из файла
    :param json_file: JSON файл c вакансиями
    :param top_n: необходимое кол-во вакансий для печати
    :return: None
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)
        if top_n > 0:
            top_n_vacancies = []
            count = 0
            for vacancy in vacancies:
                if count == top_n:
                    break
                top_n_vacancies.append(vacancy)
                count += 1

            print_vacancies(top_n_vacancies)

        else:
            print_vacancies(vacancies)


def print_vacancies(vacancies):
    """
    Печать вакансий из необходимого списка с вакансиями
    :param vacancies: вакансии из списка
    :return: печать
    """
    for vacancy in vacancies:
        salary = get_salary(vacancy)
        vacancy_info = ('------------------\n'
                        f'ID вакансии: {vacancy["id"]}\n'
                        f'Наименование вакансии: {vacancy["profession"]}\n'
                        f'Зарплата: \n{salary}'
                        f'\nСсылка: {vacancy["vacancy_url"]}\n'
                        f'Описание: {vacancy["description"]}\n')

        print(vacancy_info)


def get_salary(vacancy):
    """
    Функция для вывода на печать зарплаты при показе вакансий
    :param vacancy: вакансия в dict формате
    :return: зарпалата на печать
    """
    salary = vacancy["salary"]
    if salary != "Не указана":
        return (f'\tОт: {salary["from"]}\n'
                f'\tДо: {salary["to"]}\n'
                f'\tВалюта: {salary["currency"].upper()}')
    return f'\t{salary}'


def delete_vacancy_by_id(json_file) -> None:
    """
    Функция для удаления вакансии по его ID.

    :param json_file: JSON файл с вакансиями
    :return: JSON файл с удаленной вакансией
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        vacancies_list = json.load(f)
        validate_id = False

        while not validate_id:
            id_vacancy = check_id()  # получаем ID вакансии
            for index, vacancy in enumerate(vacancies_list):
                if vacancy["id"] == id_vacancy:
                    vacancies_list.pop(index)
                    validate_id = True
                    break
            else:
                print("Такого индекса нет в вакансиях")

        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(vacancies_list, outfile, ensure_ascii=False, indent=2)


def add_vacancy() -> Vacancy:
    """Принимает от пользователя данные и создает объект (вакансию) класса Vacancy."""
    vacancy_id = check_id()
    profession = check_profession()
    salary = check_salary()
    vacancy_url = check_vacancy_url()
    description = check_description()

    return Vacancy(vacancy_id, profession, salary, vacancy_url, description)


def sort_by_salary():
    pass


# функции валидации входных данных от пользователя
def get_top_n():
    """Функция для валидации введенной цифры."""
    validated_top_n = ''

    validate = False
    while not validate:
        input_top_n = input("Введите топ N вакансий (число больше нуля): ")
        if not input_top_n.isdigit():
            print("Введите число больше нуля, а не кто его знает что...")
        elif int(input_top_n) <= 0:
            print("Введите число больше нуля... просил же")
        else:
            validated_top_n = int(input_top_n)
            validate = True

    return validated_top_n


def check_id() -> int:
    """Функция для валидации ID вакансии."""
    validated_id = ''

    validate = False
    while not validate:
        input_vacancy_id = input("Введите ID вакансии: ")
        if not input_vacancy_id.isdigit():
            print("ID вакансии должен состоять из цифр")
        elif len(input_vacancy_id) != 8:
            print("Длина ID вакансии должно быть равным 8 (восьми)")
        else:
            validated_id = int(input_vacancy_id)
            validate = True

    return validated_id


def check_profession() -> str:
    """Функция для валидации наименования вакансии."""
    validated_profession = ''

    validate = False
    while not validate:
        input_profession = input("Введите наименование вакансии: ")
        if input_profession.isdigit():
            print("Наименование вакансии должно состоять из букв")
        elif not len(input_profession) >= 10:
            print(
                "Наименование вакансии должно состоять из минимум 10 символов.")
        else:
            validated_profession = input_profession.strip()
            validate = True

    return validated_profession


def check_salary() -> dict:
    """Функция для валидации зарплаты вакансии."""
    salary_from = ''
    salary_to = ''
    currency = ''

    from_validate = False
    to_validate = False
    currency_validate = False
    while not from_validate:
        input_from = input("Введите зарплату ОТ (только из цифр): ")
        if not input_from.isdigit():
            print("Зарплата ОТ может состоять из цифр")
        else:
            salary_from = int(input_from)
            from_validate = True

    while not to_validate:
        input_to = input("Введите зарплату ДО (только из цифр): ")
        if not input_to.isdigit():
            print("Зарплата ДО может состоять из цифр")
        elif not int(input_to) >= salary_from:
            print("Зарплата ДО должна быть больше или равна зарплаты ОТ")
        else:
            salary_to = int(input_to)
            to_validate = True

    while not currency_validate:
        input_currency = input(
            "Введите валюту в формате RUB (только из трех букв): ").upper()
        if not input_currency.isalpha():
            print("Валюта может состоять только из букв")
        elif len(input_currency) != 3:
            print("Валюта может состоять только из 3-х букв")
        else:
            currency = input_currency
            currency_validate = True

    validated_salary = {"from": salary_from,
                        "to": salary_to,
                        "currency": currency.upper(),
                        }

    return validated_salary


def check_vacancy_url() -> str:
    """Функция для валидации URL вакансии."""
    validated_url = ''

    validate = False
    while not validate:
        input_url = input(
            "Введите ссылка на вакансию (начало с https:// и окончание на .ru): ")
        if not input_url.startswith('https://'):
            print("Ссылка должна начинаться с https://")
        elif not input_url.endswith('.ru'):
            print("Ссылка должна заканчиваться на .ru")
        elif len(input_url[input_url.rfind('/') + 1:input_url.rfind('.')]) < 1:
            print("Домен должна состоять хотя бы из 1 буквы или цифры")
        else:
            validated_url = input_url
            validate = True

    return validated_url


def check_description() -> str:
    """Функция для валидации описания вакансии."""
    validated_description = ''

    validate = False
    while not validate:
        input_description = input("Введите описание вакансии: ")
        if input_description.isdigit():
            print("Наименование вакансии должно состоять из букв")
        elif not len(input_description) >= 20:
            print("Описание вакансии должно состоять минимум из 20 символов.")
        else:
            validated_description = input_description.strip()
            validate = True

    return validated_description
