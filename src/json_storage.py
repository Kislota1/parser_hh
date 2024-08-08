import json
from .vacancy_storage import VacancyStorage
from .vacancy import Vacancy
class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_vacancy(self, vacancy):
        data = self._read_file()
        data.append(vacancy.__dict__)
        self._write_file(data)

    def get_vacancies(self, **criteria):
        data = self._read_file()
        vacancies = [Vacancy(**vac) for vac in data]
        for key, value in criteria.items():
            vacancies = [vac for vac in vacancies if getattr(vac, key) == value]
        return vacancies

    def delete_vacancy(self, vacancy):
        data = self._read_file()
        data = [vac for vac in data if vac['url'] != vacancy.url]
        self._write_file(data)