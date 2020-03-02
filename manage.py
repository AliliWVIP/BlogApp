import os
from app import create_app
from app.extensions import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

# 添加命令行启动控制
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

# 使用pip按照模块可以使用国内的镜像
# pip3 install --index https://mirrors.ustc.edu.cn/pypi/web/simple/ -r requirements.txt
