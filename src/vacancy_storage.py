from abc import ABC, abstractmethod

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