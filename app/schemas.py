from pydantic import BaseModel, constr, model_validator
from typing import Literal


class Signup(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: str
    password: constr(min_length=8, max_length=25)
    password2: str
    age: int
    gender: Literal['Male', 'Female']

    @model_validator(mode="before")
    @classmethod
    def pwd_match(cls, values):
        if values['password2'] != values['password']:
            raise ValueError("Password doesn't Match")
        return values


class Login(BaseModel):
    email: str
    password: str
