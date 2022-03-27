from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, val):
        return self.session.query(User).filter(User.username == val).all()

    def get_by_role(self, val):
        return self.session.query(User).filter(User.role == val).all()

    def create(self, user_id):
        n_user = User(**user_id)
        self.session.add(n_user)
        self.session.commit()
        return n_user

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, username):
        user = self.get_by_username(username.get("username"))
        user.role = username.get("role")
        user.password = username.get("password")
        self.session.add(user)
        self.session.commit()
