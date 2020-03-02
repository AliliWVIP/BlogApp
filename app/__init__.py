# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-11 13:51'

from flask import Flask
from app.config import config
from app.extensions import config_extensions
from app.views import config_blueprint
from app.errors import config_errorhandler


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 通过类初始化配置
    app.config.from_object(config[config_name])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 配置相关扩展
    config_extensions(app)
    # 配置相关的蓝本
    config_blueprint(app)
    # 配置错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app





