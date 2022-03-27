import base64
import datetime
import hashlib
import hmac
import jwt
import calendar
from flask import current_app, request
from flask_restx import abort

def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.datetime(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])
    return {'access_token': access_token, 'refresh_token': refresh_token}

def compare_password(password_hash, other_password):
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256', other_password.encode('utf-8'), current_app.config["PWD_HASH_SALT"], current_app.config["PWD_HASH_ITERATIONS"])
    )

###############################

def generate_password(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    ))

#############################

def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, current_app.config["SECRET_HERE"], current_app.config["JWT_ALGORITHM"])
    except Exception as e:
        print("JWT Decode Exception", e)
        abort(401)
    else:
        return decoded_jwt


def auth_check():
    if "Authorization" not in request.headers:
        return False
    token = request.headers["Authorization"].split("Bearer ")[-1]
    return jwt_decode(token)


def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization Error")
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get("role")
            if role == "admin":
                return func(*args, **kwargs)
        abort(401, "Admin role required")
    return wrapper






