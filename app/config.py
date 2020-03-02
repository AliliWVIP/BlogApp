# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-10 16:12'

import os
import pymysql

base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 '\xdc\xc0\xb8\x0e\xe2\x95\xd8\xc1Z\xb1:\x85\xe5D\x92M\xe8\xca\xb8\x9b\xb0\x80\x91'
    # 数据库操作
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'aliliios@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Alili8699200'
    # 使用本地库中的bootstrap依赖包
    BOOTSTRAP_SERVE_LOCAL = True

    # 文件上传配置
    # 上传文件的最大值
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # 上传文件的存储位置
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')

    # 初始化的方法
    @staticmethod
    def init_app(app):
        pass

# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qweasd@localhost:3306/blog-dev?charset=utf8mb4"

# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname/database'

# 生成环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname/database'



# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认配置
    'default': DevelopmentConfig
}
