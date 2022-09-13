#inisialisasi objek flask
from distutils.log import debug
from flask import Flask

app = Flask(__name__)

#running app

from app import routes,models

if __name__ == '__main__':
    app.run(debug = True)

