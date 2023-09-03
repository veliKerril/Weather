from flask import render_template

class Views:
    @staticmethod
    def main_page():
        return render_template('main_page.html')

    @staticmethod
    def authorization():
        return render_template('authorization.html')

    @staticmethod
    def registration():
        return render_template('registration.html')

    @staticmethod
    def search(city):
        return render_template('search.html', city=city)

    @staticmethod
    def forecast():
        return render_template('forecast.html')
