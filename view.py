from flask import render_template

class Views:
    @staticmethod
    def main_page(all_cities):
        return render_template('main_page.html', all_cities=all_cities)

    @staticmethod
    def authorization():
        return render_template('authorization.html')

    @staticmethod
    def registration():
        return render_template('registration.html')

    @staticmethod
    def search(info_city):
        return render_template('search.html', info_city=info_city)

    @staticmethod
    def forecast():
        return render_template('forecast.html')
