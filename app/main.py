# app/main.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '[push] Hello, World!'

@app.route('/version')
def version():
    return 'this is version'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
