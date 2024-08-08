from abc import ABC, abstractmethod

class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, **criteria):
        """Получение списка вакансий по заданным критериям."""
        pass