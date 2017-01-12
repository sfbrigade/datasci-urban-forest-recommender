"""Stupid simple recomendation engine"""
from flask import Flask, render_template, send_from_directory, request, jsonify
import model
APP = Flask(__name__, template_folder='assets/templates/')

@APP.route('/')
def homepage():
    """Home"""
    return render_template('index.html')

@APP.route('/recommend/<int:latitude>/<int:longitude>')
def recomendation(latitude, longitude):
    """Calls recomendation engine. Expects latitude and longitude"""
    result = model.TreeRecommendation(lat,long)
    return jsonify(result)

@APP.route('/assets/js/<path:path>')
def send_js(path):
    """Assets including javascript"""
    return send_from_directory('assets/js', path)


if __name__ == '__main__':
    APP.run(debug=True, use_reloader=True)
