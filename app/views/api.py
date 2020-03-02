# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-20 10:48'

from flask import Blueprint, abort, jsonify, request
from app.my_auth import auth
from app.models import User
from flask_login import login_user

api = Blueprint('api', __name__)

posts = [
    {
        "id": 1,
        "title": "Python入门"
    },
    {
        "id": 2,
        "title": "Python入门2"
    }
]

# 添加登录接口
@api.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    print(request.json)
    user = User.authenticate(request.json['username'], str(request.json['password']))
    if user:
        login_user(user=user)
        token = user.generate_activate_token().decode("ascii")
        print(token)
        return jsonify({'message': '登录成功', 'token': token}), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401

# 添加Restful的API接口
@api.route('/posts', methods=['GET'])
# 添加认证（路由保护）
@auth.login_required
def get_posts_list():
    return jsonify({'posts': posts})

@api.route('/posts/<int:pid>', methods=['GET'])
@auth.login_required
def get_posts(pid):
    p = list(filter(lambda t: t['id'] == pid, posts))
    if len(p) == 0:
        abort(404)
    return jsonify({"post": p[0]})


@api.route('/posts', methods=['POST'])
def create_posts():
    if not request.json or 'title' not in request.json:
        abort(400)
    post = {
        "id": posts[-1]['id'] + 1,
        "title": request.json["title"]
    }
    posts.append(post)
    return jsonify({"posts": post}), 201

@api.route('/posts/<int:pid>', methods=['PUT'])
def update_posts(pid):
    p = list(filter(lambda t: t['id'] == pid, posts))
    if len(p) == 0:
        abort(404)
    if 'title' in request.json:
        p[0]["title"] = request.json.get('title')
    return jsonify({'posts': p[0]})

@api.route('/posts/<int:pid>', methods=['DELETE'])
def delete_posts(pid):
    p = list(filter(lambda t: t['id'] == pid, posts))
    if len(p) == 0:
        abort(404)
    posts.remove(p[0])
    return jsonify({'result': "数据已删除"})


@api.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found', 'status': 404}), 404

@api.errorhandler(400)
def bad_request(e):
    return jsonify({'error': '数据不完整', 'status': 400}), 400

@auth.error_handler
def unauthorized():
    return jsonify({'error': '没有认证', 'status': 401}), 401

