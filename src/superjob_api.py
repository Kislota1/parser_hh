import requests
from .vacancy_api import VacancyAPI


class SuperJobAPI(VacancyAPI):
    BASE_URL = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, api_key="v3.r.138513859.56cfc804ad6dfb7108b0d64b94627621516c84c0.f230d0832e988f2528cd89927e343a087f1a1af3"):
        self.api_key = api_key

    def get_vacancies(self, keyword, count=10):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'keyword': keyword, 'count': count}
        response = requests.get(self.BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()