import requests
from .vacancy_api import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, text, per_page=10):
        params = {'text': text, 'per_page': per_page}
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()