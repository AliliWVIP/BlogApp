# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-11 14:52'

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, PasswordForm, AvatarForm
from app.email import send_mail
from app.models import User
from app.extensions import db, photos
from flask_login import login_user, logout_user, login_required, current_user
from app.my_rand import rand_str
import os
from PIL import Image


user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建对象
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 写入数据库
        db.session.add(u)
        # 因为下面产生token时需要用到用户id,此时还没有用户id
        db.session.commit()
        # 生成token
        token = u.generate_activate_token()
        # 发送激活邮件
        send_mail(form.email.data, '账户激活', 'email/account_active', token=token, username=form.username.data)
        flash('激活邮件已发送，请点击链接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

@user.route('/activate/<token>')
def activate(token):
    if check_activate_token(token):
        print('激活成功')
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        print('激活失败')
        flash('账户激活失败')
        return redirect(url_for('main.index'))



@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('用户名不存在')
        elif u.verify_password(form.password.data):
            # 验证通过，用户登录, 顺便完成记住我的功能
            login_user(u, remember=form.remember_me.data)
            # 如果有下一跳就跳转到指定地址，没有就跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            db.session.add(current_user)
            flash('密码修改成功，请使用新密码重新登录')
            logout_user()
            return redirect(url_for('user.login'))
        else:
            flash('原密码错误')
            return redirect(url_for('user.change_password'))
    return render_template('user/change_password.html', form=form)

@user.route('/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        # 生成随机的文件名
        suffix = os.path.splitext(form.avatar.data.filename)[1]
        name = rand_str() + suffix
        photos.save(form.avatar.data, name=name)
        # 生成缩略图
        pathname = os.path.join(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name))
        img = Image.open(pathname)
        img.thumbnail((128, 128))
        img.save(pathname)
        # 删除原有头像
        if current_user.avatar != 'default.png':
            # 第一次更换头像不删除
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.avatar))
        current_user.avatar = name
        db.session.add(current_user)
        flash('头像已上传成功')
    return render_template('user/change_avatar.html', form=form)

