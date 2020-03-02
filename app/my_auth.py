# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-21 14:40'

# 认证
from flask_httpauth import HTTPBasicAuth
from app.models.user import User

auth = HTTPBasicAuth()

# 设置认证的回调函数，需要认证时自动回调，成功返回True，失败返回False
@auth.verify_password
def verify_password(username_or_token, password):


    # print(username_or_token)
    # user = check_activate_token(username_or_token)
    # print(user)
    # if not user:
    #     return False
    # else:
    #     return True
    # print(username_or_token)
    u = User.query.filter_by(username = username_or_token).first()
    if u and u.verify_password(password):
        return True
    else:
        if User.check_activate_token(username_or_token):
            return True
        return False


