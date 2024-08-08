from .headhunter_api import HeadHunterAPI
from .superjob_api import SuperJobAPI
from .json_storage import JSONVacancyStorage
from .vacancy import Vacancy

class UserInteraction:
    def __init__(self):
        self.api = None
        self.storage = JSONVacancyStorage('vacancies.json')

    def run(self):
        while True:
            print("1. Выбрать платформу (HeadHunter/SuperJob)")
            print("2. Найти вакансии")
            print("3. Показать вакансии")
            print("4. Удалить вакансию")
            print("5. Выйти")
            choice = input("Выберите действие: ")

            if choice == '1':
                self.choose_platform()

            elif choice == '2':
                if not self.api:
                    print("Сначала выберите платформу!")
                else:
                    self.search_vacancies()

            elif choice == '3':
                self.show_vacancies()

            elif choice == '4':
                self.delete_vacancy()

            elif choice == '5':
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    def choose_platform(self):
        platform = input("Введите платформу для поиска вакансий (HeadHunter/SuperJob): ").strip().lower()
        if platform == "headhunter":
            self.api = HeadHunterAPI()
        elif platform == "superjob":
            self.api = SuperJobAPI()
        else:
            print("Неверная платформа. Попробуйте снова.")

    def search_vacancies(self):
        text = input("Введите поисковый запрос: ")
        per_page = int(input("Сколько вакансий показать: "))
        vacancies_data = self.api.get_vacancies(text=text, per_page=per_page)
        for vacancy_data in vacancies_data['items']:
            title = vacancy_data['name']
            url = vacancy_data['alternate_url']
            salary = vacancy_data['salary']
            salary_from = salary['from'] if salary else None
            salary_to = salary['to'] if salary else None
            description = vacancy_data['snippet']['requirement']
            vacancy = Vacancy(title, url, salary_from, salary_to, description)
            self.storage.add_vacancy(vacancy)
            print(f"Добавлена вакансия: {vacancy}")

    def show_vacancies(self):
        criteria = {}
        key = input("Введите критерий для поиска (например, title): ")
        value = input("Введите значение критерия: ")
        criteria[key] = value
        vacancies = self.storage.get_vacancies(**criteria)
        for vacancy in vacancies:
            print(vacancy)

    def delete_vacancy(self):
        url = input("Введите URL вакансии для удаления: ")
        vacancies = self.storage.get_vacancies(url=url)
        for vacancy in vacancies:
            self.storage.delete_vacancy(vacancy)
            print(f"Вакансия удалена: {vacancy}")


