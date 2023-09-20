from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from .auth import auth
from .views import views
from .models import Base
from .config import settings

app = Flask(__name__)
jwt = JWTManager(app)
cors = CORS(app)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PW}@{settings.DB_HOST}:\
{settings.DB_PORT}/{settings.DB_NAME}'

if not database_exists(url=SQLALCHEMY_DATABASE_URL):
    create_database(url=SQLALCHEMY_DATABASE_URL)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
session = Session(engine)

app.register_blueprint(auth)
app.register_blueprint(views)
