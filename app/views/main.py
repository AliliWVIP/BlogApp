# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-11 14:43'

from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/', methods = ['POST', 'GET'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            # 根据表单提交的数据常见对象
            p = Posts(content=form.content.data, user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才能发表博客')
            return redirect(url_for('user.login'))
    # 从数据库读取博客，并分配到模板中，然后在模板中渲染
    # posts = Posts.query.filter_by(rid == 0).order_by(Posts.timestamp.desc()).all()
    # 分页处理

    # 获取当前页码， 没有默认是第一页
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=2, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)



