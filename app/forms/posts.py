# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-18 17:56'

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostsForm(FlaskForm):
    # 如果想要设置字段的其他属性，可以通过render_kw完成
    content = TextAreaField('', render_kw = {'placeholder': '这一刻的想法...'},
                            validators=[DataRequired(), Length(1, 128, message="内容长度必须为1到128")])
    submit = SubmitField('发表')


