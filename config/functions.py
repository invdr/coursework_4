import json

from config.classes import Vacancy


def delete_vacancy_in_json(json_file) -> None:
    """Функция для удаления вакансии по его ID."""
    with open(json_file, 'r', encoding='utf-8') as f:
        vacancies_list = json.load(f)
        validate_id = False

        while not validate_id:
            id_vacancy = check_id()
            for index, vacancy in enumerate(vacancies_list):
                if vacancy["id"] == id_vacancy:
                    vacancies_list.pop(index)
                    validate_id = True
                    break
            else:
                print("Такого индекса нет в вакансиях")

        with open(json_file, 'w', encoding='utf-8') as outfile:
            json.dump(vacancies_list, outfile, ensure_ascii=False, indent=2)


def input_vacancy_info() -> Vacancy:
    """Принимает от пользователя данные и создает объект (вакансию) класса Vacancy."""
    vacancy_id = check_id()
    profession = check_profession()
    salary = check_salary()
    vacancy_url = check_vacancy_url()
    description = check_description()

    return Vacancy(vacancy_id, profession, salary, vacancy_url, description)


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
            print("Наименование вакансии должно состоять из минимум 10 символов.")
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
        input_currency = input("Введите валюту в формате RUB (только из трех букв): ").upper()
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
        input_url = input("Введите ссылка на вакансию (начало с https:// и окончание на .ru): ")
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
