import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PW = os.getenv('DB_PW')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')


settings = Settings()
