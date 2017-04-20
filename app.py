"""Stupid simple recomendation engine"""
import os
from flask import Flask, render_template, send_from_directory, jsonify, abort
from model import TreeRecommendation

APP = Flask(__name__, template_folder='assets/templates/')
RECOMMENDER = TreeRecommendation()

@APP.route('/')
def homepage():
    """Home"""
    return render_template('index.html', key=os.environ.get('GOOGLE_MAPS_API_KEY'))


@APP.route('/data')
def data():
    """Print raw data as html"""
    return RECOMMENDER.data_html()


@APP.route('/recommend/<latitude>/<longitude>')
def recomendation(latitude, longitude):
    """Calls recomendation engine. Expects latitude and longitude"""
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        abort(404)
    result = RECOMMENDER.recommend(latitude, longitude)
    return jsonify(result)


@APP.route('/assets/js/<path:path>')
def send_js(path):
    """Assets including javascript"""
    return send_from_directory('assets/js', path)


if __name__ == '__main__':
    APP.run(debug=True, use_reloader=True)
