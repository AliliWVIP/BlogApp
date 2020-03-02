# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-11 14:44'

from .main import main
from .user import user
from .api import api
from .apiv2 import apiV2

DEFAULT_BLUEPRINT = (
    (main, ''),
    (user, '/user'),
    (api, '/api'),
    (apiV2, '/apiV2')
)


# 配置相关的蓝本
def config_blueprint(app):
    for blue_print, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print, url_prefix= url_prefix)

