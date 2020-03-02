# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-21 11:14'
from flask import jsonify, Blueprint
from app.extensions import api
from app.my_auth import auth
from flask_restful import Resource, reqparse
from flask_login import login_user, login_required
from app.models import User

apiV2 = Blueprint('apiV2', __name__)

# 创建资源，继承自Resource
class UserAPI(Resource):


    def get(self, id):
        return {'User': 'GET'}

    def put(self, id):
        return {'User': 'PUT'}

    def delete(self, id):
        return {'User': 'Delete'}

# 添加资源
# 参数一 资源的类名
# 参数二 路由地址，可以是多个
# 参数三 endpoint: 端点
api.add_resource(UserAPI, '/apiV2/user/<int:id>', '/u/<int:id>', endpoint='user')

class UserListAPI(Resource):
    # 添加认证（资源保护）
    decorators = [auth.login_required]
    def get(self):
        return {'UserList': 'GET'}

    def put(self):
        return {'UserList': 'PUT'}

    def delete(self):
        return {'UserList': 'Delete'}

api.add_resource(UserListAPI, '/apiV2/user', endpoint='users')


class LoginAPI(Resource):

    def post(self):
        parse = reqparse.RequestParser()\
            .add_argument('username', type=str, location='json', required=True, help="用户名不能为空")\
            .add_argument('password', type=str, location='json', required=True, help="密码不能为空")
        args = parse.parse_args()
        user = User.authenticate(args['username'], args['password'])
        if user:
            login_user(user=user)
            token = user.generate_activate_token().decode("utf-8")
            print(token)
            return {'message': '登录成功', 'token': token}, 200
        else:
            return {'message': '用户名或密码错误'}, 401

api.add_resource(LoginAPI, '/apiV2/login', endpoint='login')


class Protected(Resource):
    decorators = [auth.login_required]
    def get(self):
        return {'message': '这是需要Token的GET方法'}, 200

    @login_required
    def post(self):
        return {'message': '这是需要Token的POST方法'}, 201

api.add_resource(Protected, '/apiV2/protected', endpoint='protected')




@apiV2.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found', 'status': 404}), 404

@apiV2.errorhandler(400)
def bad_request(e):
    return jsonify({'error': '数据不完整', 'status': 400}), 400

@auth.error_handler
def unauthorized():
    return jsonify({'error': '没有认证', 'status': 401}), 401
