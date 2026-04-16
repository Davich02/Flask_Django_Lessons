from datetime import datetime

from pydantic import BaseModel, EmailStr, ValidationError, Field, field_validator


# модель адреса, используется как вложенное поле в модели пользователя
class Address(BaseModel):
    city: str
    street: str
    house_number: int


# модель пользователя с конфигурацией, валидатором почты и автоматической датой создания
class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    created_at: datetime = datetime.now()  # дата создания — автоматически ставится текущее время
    is_active: bool = True
    address: Address

    # старый способ конфигурации через вложенный класс Config (pydantic v1)
    # class Config:
    #     str_min_length = 2
    #     str_strip_whitespace = True
    #     json_encoders = {
    #         datetime: lambda v: v.strftime('%y-%m-%d %H:%M')
    #     }

    # новый способ конфигурации (pydantic v2)
    model_config = dict(
        str_min_length=2,  # минимальная длина любой строки — 2 символа
        str_strip_whitespace=True,  # автоматически убирает пробелы по краям строк
        json_encoders={  # формат сериализации даты в JSON
            datetime: lambda v: v.strftime('%y-%m-%d %H:%M')
        }
    )

    # кастомный валидатор — проверяет, что почта только с разрешённых доменов
    @field_validator('email')
    def check_email_domain(cls, value):
        allowed_domains = ['example.com', 'test.com']
        email_domain = value.split('@')[-1]  # берём часть после @
        if email_domain not in allowed_domains:
            raise ValueError(f"Email must be from one of the following domains: {', '.join(allowed_domains)}")
        return value

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

    def __str__(self):
        return f"User {self.name}, {self.age} years old. Email: {self.email}. City: {self.address.city}"


# модель администратора, наследуется от User и добавляет поля для прав доступа
class AdminUser(User):
    is_superuser: bool
    access_level: int

    def __str__(self):
        return f"Admin {self.name}, Email: {self.email}, Access Level: {self.access_level}"

    # повышение уровня доступа администратора на 1
    def promote_user(self):
        self.access_level = self.access_level + 1


# модель товара с использованием Field для тонкой настройки полей
class Item(BaseModel):
    # alias — позволяет принимать данные под именем "available", но хранить как is_available
    is_available: bool = Field(default=True, alias="available", description="Whether the item is available for order")
    # gt=0 — цена должна быть строго больше нуля, иначе ошибка валидации
    price: float = Field(default=0.0, gt=0, description="The price of the item must be greater than zero")


if __name__ == '__main__':
    # пример работы с Item :
    # item = Item(available=False, price=0.0)  # передаём "available", а не "is_available" (благодаря alias)
    # print(item.is_available)  # обращаемся к полю по его настоящему имени
    # print(item.price)

    # JSON-строка с данными для администратора
    json_string = """{
        "id": 1,
        "name": "John Doe",
        "age": 22,
        "email": "john.doe@test.com",
        "is_active": false,
        "is_superuser": false,
        "access_level": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    # десериализация JSON в объект AdminUser (strict — без автоприведения типов)
    admin = AdminUser.model_validate_json(json_string,
                                          strict=True)
    print(admin.__repr__)  # выводит ссылку на метод repr (для вызова нужны скобки: __repr__())
    print(admin.model_dump_json())  # сериализация объекта обратно в JSON-строку