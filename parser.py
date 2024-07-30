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



