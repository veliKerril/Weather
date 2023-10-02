from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'authorization'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"


from . import model
from . import controller

