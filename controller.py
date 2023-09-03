from flask import Flask, request, redirect, url_for
from view import Views
"Временное решение - пускай пока приложение запускается отсюда."
"Надо сделать так, чтобы контроллер был завернут в один какой-нибудь класс"
"И, при этом, запуск приложения происходит из другого файла"

cities = {
    'Moscow': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Saint-Petersburg': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Rostov-on-Don': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
    'Yekaterinburg': {'temperature': 123, 'info1': 1, 'info2': 3, 'info3': 3},
}


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
    return Views.main_page()


@app.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    return Views.search(city=city)


@app.route('/forecast', methods=['GET'])
def forecast():
    return Views.forecast()


if __name__ == '__main__':
    app.run(debug=True)
