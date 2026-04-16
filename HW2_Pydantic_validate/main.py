from pydantic import BaseModel, EmailStr, ValidationError, Field, model_validator, field_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('name')
    def check_name(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError("Имя должно содержать только буквы")
        return value


    @model_validator(mode='after')
    def check_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(f"Работающий пользователь должен быть от 18 до 65 лет, а указан возраст {self.age}")
        return self


def register_user(json_input: str) -> str:
    try:
        user = User.model_validate_json(json_input)
        print(f"User {user.name} registered successfully!")
        return user.model_dump_json()
    except ValidationError as e:
        return str(e)


if __name__ == '__main__':
    user_data = ('{"name": "John", "age": 30, "email": "pushka@gmail.com", "is_employed": true,'
                 ' "address": {"city": "New York", "street": "Main Street", "house_number": 123}}')
    user_data2 = ('{"name": "John Doe", "age": 70, "email": "john.doe@example.com", "is_employed": true,'
                  ' "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}}')
    user_data3 = ('{"name": "J", "age": 40, "email": "john.doe@example.com", "is_employed": true,'
                  ' "address": {"city": "New York", "street": "5th Avenue", "house_number": 123}}')
    user_data4 = ('{"name": "John123", "age": 30, "email": "test@gmail.com", "is_employed": false,'
                  ' "address": {"city": "NY", "street": "Main St", "house_number": 5}}')
    print(register_user(user_data))
    print(register_user(user_data2))
    print(register_user(user_data3))
    print(register_user(user_data4))