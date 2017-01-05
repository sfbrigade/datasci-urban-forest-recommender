from flask import Flask, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__, template_folder='assets/templates/')

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return render_template('index.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route('/assets/js/<path:path>')
def send_js(path):
    return send_from_directory('assets/js', path)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)