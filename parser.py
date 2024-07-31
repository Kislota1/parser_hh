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

