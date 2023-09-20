from passlib.context import CryptContext
from flask import request
from sqlalchemy import select
from . models import RevokedToken


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password):
    return pwd_context.hash(password)


def verify_password(input_pw, original_pw):
    return pwd_context.verify(input_pw, original_pw)


def get_token():
    header = request.headers['Authorization']
    token = header.split(' ')[1]

    return token


def check_logout_status():
    from . import session

    token = get_token()

    if session.execute(select(RevokedToken).where(RevokedToken.revtoken == token)).first():
        return True
