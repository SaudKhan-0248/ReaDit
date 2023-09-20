from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from .schemas import Signup, Login
from .models import User, RevokedToken
from .utils import hash, verify_password, get_token

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():
    try:
        data = Signup(**request.json)
    except ValidationError as error:
        return jsonify({"Error": str(error)}), 400

    username = data.username
    email = data.email
    password = hash(data.password)
    age = data.age
    gender = data.gender

    user = User(username=username, email=email,
                password=password, age=age, gender=gender)

    from . import session

    try:
        session.add(user)
        session.commit()

    except IntegrityError:
        session.rollback()
        abort(409, "message: User already exists!")

    return jsonify({"message": "User Created Successfully!"}), 200


@auth.route('/login', methods=['POST'])
def login():
    try:
        data = Login(**request.json)
    except ValidationError as error:
        return jsonify({"Error": str(error)}), 400

    email = data.email
    password = data.password

    from . import session

    query = select(User).where(User.email == email)
    record = session.execute(query).first()

    if not record:
        abort(403, "Error: Wrong Credentials")

    else:
        user = record[0]
        if verify_password(password, user.password):
            token = create_access_token(
                identity=user.id, expires_delta=timedelta(minutes=30))
            return {"token": token}, 200

        else:
            abort(403, "Error: Wrong Credentials")


@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    token = get_token()

    from . import session

    revoked_token = RevokedToken(revtoken=token)

    try:
        session.add(revoked_token)
        session.commit()

    except IntegrityError:
        session.rollback()
        abort(401, "message: Unauthorized to perform requested acion")

    return jsonify({"message": "Logged out Successfully!"})
