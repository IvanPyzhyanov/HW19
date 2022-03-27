from flask import request
from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from implemented import user_service
from tools.security import auth_required, admin_required


user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        username = request.args.get("username")
        role = request.args.get("role")
        filters = {
            "username": username,
            "role": role,
        }
        all_users = user_service.get_all(filters)
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        req = user_service.get_one(uid)
        return UserSchema().dump(req), 200

    @auth_required
    @admin_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    @auth_required
    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
