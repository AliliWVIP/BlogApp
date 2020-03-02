# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-10 16:12'

# 导入相关扩展类库
from flask_bootstrap import Bootstrap
# 邮件
from flask_mail import Mail
# 时间
from flask_moment import Moment
# 数据库
from flask_sqlalchemy import SQLAlchemy
# 登录
from flask_login import LoginManager
# 上传文件
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
# restful 第三方
from flask_restful import Api




# 创建相关扩展对象
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)
api = Api()


# 配置相关扩展
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    # 会话保护级别 None 不使用 basic 基本级别 strong 用户信息更改立即退出
    login_manager.session_protection = 'strong'
    # 设置登录页面端点, 当用户访问需要登录才能访问的页面，此时还没有登录，自动跳转到此处
    login_manager.login_view = 'user.login'
    # 设置提示信息，默认是英文提示信息
    login_manager.login_message = '需要登录才可访问'

    api.init_app(app)
    # 上传文件初始化
    configure_uploads(app, photos)
    patch_request_class(app, size=None)


