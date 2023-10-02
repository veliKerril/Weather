from app import app, db
from flask import request, flash, redirect, url_for
from sqlalchemy import exc
from .view import Views
from .service import CityWeather, ContainerCities, ForecastCity
from .model import Users, Location
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    # Обработка случая, когда пользователь нажал на кнопку "Авторизоваться"
    # Если же пользователь просто зашел на страницу авторизации, то ему предоставится ее форма
    if request.method == "POST":
        email = request.form.get('email')
        psw = request.form.get('psw')
        user = db.session.query(Users).filter(Users.email == email).first()
        if user and check_password_hash(user.psw, psw):
            login_user(user, remember=True)
            return redirect(url_for('main_page'))
        elif len(email) == 0 or len(psw) == 0:
            flash('Заполните все поля')
        elif not user:
            flash("Такой email не зарегистрирован")
        elif not check_password_hash(user.psw, psw):
            flash('Неверный пароль')
    return Views.authorization()


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        psw = request.form.get('psw')
        psw2 = request.form.get('psw2')
        if len(name) > 3 and len(psw) > 4 and psw == psw2:
            try:
                user_hash = generate_password_hash(psw)
                u = Users(name=name, email=email, psw=user_hash)
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('authorization'), 301)
            # Так как email уникальный, то при попытке создать пользователя с уже существующим email
            # дропнется эта ошибка
            except exc.IntegrityError:
                flash('Пользователь с таким email уже существует')
            except:
                db.session.rollback()
                print('Ошибка добавления в бд')
        elif len(name) == 0 or len(email) == 0 or len(psw) == 0 or len(psw2) == 0:
            flash('Все поля должны быть заполнены')
        elif len(name) <= 3:
            flash('Имя пользователя должно состоять хотя бы из четырех символов')
        elif len(psw) <= 4:
            flash('Пароль должен состоять хотя бы из 5 символов')
        elif psw != psw2:
            flash('Введенные пароли должны совпадать')
    return Views.registration()


@app.route('/main-page', methods=['GET', 'POST'])
@app.route('/')
def main_page():
    # Если мы удаляем город, то через post передаем информацию об имени города
    if request.method == 'POST':
        name = request.form.get('city_name')
        try:
            del_city = db.session.query(Location).filter(Location.user_id == current_user.get_id(),
                                                         Location.city == name).first()
            db.session.delete(del_city)
            db.session.commit()
        except:
            db.session.rollback()
            print('Ошибка удаления города')

    cities = db.session.query(Location).filter(Location.user_id == current_user.get_id()).all()
    all_cities = ContainerCities.del_and_get_all_cities(cities)
    return Views.main_page(all_cities)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # Обработчик нажатия на кнопку "Поиск"
    if request.method == 'GET':
        try:
            city = request.args.get('city').strip()
            if len(city) == 0:
                flash('Введите название города в строке поиска')
                return Views.search()
            info_city = CityWeather(city)
            return Views.search(info_city=info_city)
        except:
            flash('Не удалось найти подходящий город')
            return Views.search()
    # Обработчик добавления города в избранное
    elif request.method == 'POST':
        if current_user.is_authenticated:
            try:
                city_name = request.form.get('city_name')
                # Проверка на то, чтобы нельзя было два раза добавить один и тот же город
                if not db.session.query(Location).filter(Location.user_id == current_user.get_id(),
                                                         Location.city == city_name).first():
                    location = Location(city=city_name, user_id=int(current_user.get_id()))
                    db.session.add(location)
                    db.session.commit()
            except:
                db.session.rollback()
                print('Ошибка при добавлении города')
            return redirect(url_for('main_page'), 301)
        else:
            flash('Авторизуйтесь для добавления городов в избранное')
            return redirect(url_for('authorization'), 301)


@app.route('/forecast', methods=['GET'])
@login_required
def forecast():
    city = request.args.get('city-name')
    forecast_info = ForecastCity(city).get_forecast()
    return Views.forecast(forecast_info)


@app.route('/logout_main')
def logout():
    logout_user()
    return redirect(url_for('main_page'))
