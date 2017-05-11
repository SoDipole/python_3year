from flask import Flask
from flask import url_for, render_template, request
from pymystem3 import Mystem

app = Flask(__name__)
m = Mystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text')
def text():
    return render_template('text.html')

if __name__ == '__main__':
    app.run()