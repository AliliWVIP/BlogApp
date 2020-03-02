# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-16 20:16'

from app.extensions import db
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 指定外键（表名.字段）
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))





