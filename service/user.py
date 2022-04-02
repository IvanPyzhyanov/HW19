from dao.user import UserDAO
from tools.security import generate_password


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self, filters):
        if filters.get("username") is not None:
            users = self.dao.get_by_username(filters.get("username"))
        elif filters.get("role") is not None:
            users = self.dao.get_by_role(filters.get("role"))
        else:
            users = self.dao.get_all()
        return users

    def get_by_username(self, val):
        return self.dao.get_by_username(val)

    def get_by_role(self, val):
        return self.dao.get_by_role(val)

    def create(self, user_id):
        user_id['password'] = generate_password(user_id["password"])
        return self.dao.create(user_id)

    def update(self, username):
        username['password'] = generate_password(username["password"])
        self.dao.update(username)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

