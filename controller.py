from flask import Flask, request, redirect, url_for, flash, g, login_user
from view import Views
from service import CityWeather, ContainerCities, ForecastCity
from werkzeug.security import generate_password_hash, check_password_hash
from model import Model, DataBase
from flask_login import LoginManager
from user_login import UserLogin
import os
import sqlite3

"Временное решение - пускай пока приложение запускается отсюда."
"Надо сделать так, чтобы контроллер был завернут в один какой-нибудь класс"
"И, при этом, запуск приложения происходит из другого файла"

# Конфигурация - вынести в main.
DATABASE = '/Weather.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'Weather.db')))
login_manager = LoginManager(app)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     print(email, password)
    #     return redirect(url_for('main_page'))
    # return Views.authorization()

    # if current_user.is_authenticated:
    #     return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    # return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")
    return Views.authorization()


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        psw = request.form.get('psw')
        psw2 = request.form.get('psw2')
        print(name, email, psw, psw2)
        if len(request.form.get('name')) > 4 and len(request.form.get('email')) > 4 \
                and len(request.form.get('psw')) > 4 and request.form.get('psw') == request.form.get('psw2'):
            hash = generate_password_hash(request.form['psw'])
            dbase.add_user(request.form['name'], request.form['email'], hash)
            return redirect(url_for('authorization'), 301)
    return Views.registration()


@app.route('/main-page', methods=['GET', 'POST'])
@app.route('/')
def main_page():
    if request.method == 'POST':
        name = request.form.get('city_name')
        ContainerCities.del_city(name)
    all_cities = ContainerCities.get_all_cities()
    return Views.main_page(all_cities)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        ContainerCities.add_city(city_name)
        return redirect(url_for('main_page'))
    else:
        city = request.args.get('city')
        info_city = CityWeather(city)
        return Views.search(info_city=info_city)


@app.route('/forecast', methods=['GET'])
def forecast():
    city = request.args.get('city-name')
    forecast_info = ForecastCity(city).get_forecast()
    print(forecast_info)
    for elem in forecast_info:
        print(forecast_info[elem]['time'])
    return Views.forecast(forecast_info)


if __name__ == '__main__':
    app.run(debug=True)
