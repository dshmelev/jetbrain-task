# app/main.py

import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '[push] Hello, World!'

@app.route('/version')
def version():
    return 'this is version'

@app.route('/message')
def message():
    return os.getenv("APP_MESSAGE", "APP_MESSAGE is not set")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
