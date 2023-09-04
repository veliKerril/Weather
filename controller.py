from flask import Flask, request, redirect, url_for
from view import Views
from model import CityWeather, ContainerCities

"Временное решение - пускай пока приложение запускается отсюда."
"Надо сделать так, чтобы контроллер был завернут в один какой-нибудь класс"
"И, при этом, запуск приложения происходит из другого файла"


app = Flask(__name__)


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        return redirect(url_for('main_page'))
    return Views.authorization()


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        return redirect(url_for('main_page'))
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
    return Views.forecast()


if __name__ == '__main__':
    app.run(debug=True)
