# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-11 22:03'
from flask import render_template, jsonify
from app.views import api


# 配置错误显示
def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')



