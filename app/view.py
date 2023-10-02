from flask import render_template
from flask_login import current_user


class Views:
    @staticmethod
    def main_page(all_cities):
        return render_template('main_page.html', all_cities=all_cities, current_user=current_user)

    @staticmethod
    def authorization():
        return render_template('authorization.html', current_user=current_user)

    @staticmethod
    def registration():
        return render_template('registration.html', current_user=current_user)

    @staticmethod
    def search(info_city=None):
        return render_template('search.html', info_city=info_city, current_user=current_user)

    @staticmethod
    def forecast(forecast_info):
        return render_template('forecast.html', forecast_info=forecast_info, current_user=current_user)

