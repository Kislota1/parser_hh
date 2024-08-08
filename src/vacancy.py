class Vacancy:
    def __init__(self, title, url, salary_from=None, salary_to=None, currency=None, description=None):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.description = description

        # Валидация зарплаты при инициализации
        self.validate()

    def validate(self):
        if (self.salary_from is not None and not isinstance(self.salary_from, (int, float))) or \
           (self.salary_to is not None and not isinstance(self.salary_to, (int, float))):
            raise ValueError("Зарплата должна быть числом.")

    def __lt__(self, other):
        if self.salary_from is None or other.salary_from is None:
            raise ValueError("Нельзя сравнивать вакансии, у которых не указана минимальная зарплата.")
        return self.salary_from < other.salary_from

    def __repr__(self):
        return (f"Vacancy(title={self.title}, url={self.url}, salary_from={self.salary_from}, "
                f"salary_to={self.salary_to}, currency={self.currency}, description={self.description})")
