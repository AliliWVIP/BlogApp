# -*- coding: utf-8 -*-

__author__ = 'wangli'
__date__ = '2020-02-14 22:02'

# 生成随机的字符串
def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))

