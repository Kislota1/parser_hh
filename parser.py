import json
import requests
from abc import ABC, abstractmethod


# Абстрактный класс для работы с API сайтов с вакансиями
class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query, location, num_vacancies):
        pass


# Класс для работы с API HeadHunter
class HeadHunterAPI(JobAPI):
    def get_vacancies(self, query, location, num_vacancies):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': query,
            'area': location,
            'per_page': num_vacancies
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            return []


# Класс для хранения информации о вакансии
class Vacancy:
    def __init__(self, title, url, salary_from, salary_to, description):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __str__(self):
        return f"{self.title} - {self.salary_from}-{self.salary_to} - {self.url}"

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __eq__(self, other):
        return self.salary_from == other.salary_from


# Абстрактный класс для работы с хранилищем вакансий
class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


# Класс для работы с JSON файлом
class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        data = self._read_file()
        data.append(vacancy.__dict__)
        self._write_file(data)

    def get_vacancies(self, **criteria):
        data = self._read_file()
        return [Vacancy(**vac) for vac in data if all(vac.get(key) == value for key, value in criteria.items())]

    def delete_vacancy(self, vacancy):
        data = self._read_file()
        self._write_file([vac for vac in data if vac['url'] != vacancy.url])

    def _read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)


# Функция для взаимодействия с пользователем
def user_interaction():
    api = HeadHunterAPI()
    storage = JSONVacancyStorage('vacancies.json')

    while True:
        print("1. Найти вакансии")
        print("2. Показать вакансии")
        print("3. Удалить вакансию")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            query = input("Введите поисковый запрос: ")
            location = input("Введите код региона: ")
            num_vacancies = int(input("Сколько вакансий показать: "))
            vacancies_data = api.get_vacancies(query, location, num_vacancies)
            for vacancy_data in vacancies_data:
                title = vacancy_data['name']
                url = vacancy_data['alternate_url']
                salary = vacancy_data['salary']
                salary_from = salary['from'] if salary else None
                salary_to = salary['to'] if salary else None
                description = vacancy_data['snippet']['requirement']
                vacancy = Vacancy(title, url, salary_from, salary_to, description)
                storage.add_vacancy(vacancy)
                print(f"Добавлена вакансия: {vacancy}")

        elif choice == '2':
            criteria = {}
            key = input("Введите критерий для поиска (например, title): ")
            value = input("Введите значение критерия: пример Software Engineer ")
            criteria[key] = value
            vacancies = storage.get_vacancies(**criteria)
            for vacancy in vacancies:
                print(vacancy)

        elif choice == '3':
            url = input("Введите URL вакансии для удаления: ")
            vacancies = storage.get_vacancies(url=url)
            for vacancy in vacancies:
                storage.delete_vacancy(vacancy)
                print(f"Вакансия удалена: {vacancy}")

        elif choice == '4':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == '__main__':
    user_interaction()