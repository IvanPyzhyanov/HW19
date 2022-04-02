from service.user import UserService
from tools.security import compare_password, generate_token
from flask import abort, current_app
import jwt



class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(401)

        if not is_refresh:
            if not compare_password(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "password": user.password
        }

        return generate_token(data)

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=current_app.config["SECRET_HERE"], algorithms=current_app.config["JWT_ALGORITHM"])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)

