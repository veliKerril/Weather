from flask import Flask, request, redirect, url_for, flash, g
from view import Views
from service import CityWeather, ContainerCities, ForecastCity
from werkzeug.security import generate_password_hash, check_password_hash
from model import Model, DataBase
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
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
login_manager.login_view = 'authorization'

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
    if request.method == "POST":
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['password'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin, remember=False)
            return redirect(url_for('main_page'), 301)
        flash("Неверная пара логин/пароль", "error")
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
    print(current_user, type(current_user), '1')
    return Views.registration()


@app.route('/main-page', methods=['GET', 'POST'])
@app.route('/')
def main_page():
    if request.method == 'POST':
        name = request.form.get('city_name')
        dbase.del_city_by_user_id(current_user.get_id(), name)
    # Здесь у меня списком вернутся все города, которые надо добавить в контейнер
    cities = dbase.get_cities_by_user_id(current_user.get_id())
    all_cities = ContainerCities.del_and_get_all_cities(cities)

    return Views.main_page(all_cities)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if current_user.is_authenticated:
            '''
            И именно здесь достаем информацию, которую добавляем в базу данных
            '''
            city_name = request.form.get('city_name')
            print(city_name, type(current_user.get_id()))
            dbase.add_city_with_user_id(city_name, int(current_user.get_id()))
            ContainerCities.add_city(city_name)
            return redirect(url_for('main_page'), 301)
        else:
            return redirect(url_for('authorization'), 301)
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'), 301)


if __name__ == '__main__':
    app.run(debug=True)
