# import os
from app import app, db
# from app.models import User, Post, Tag, Category, Employee, Feedback
from flask_script import Manager, Shell
# from flask_migrate import MigrateCommand

manager = Manager(app)


# Необходимая функция для неявной передачи в оболочку объектов
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag,  Category=Category, Employee=Employee, Feedback=Feedback)


manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
