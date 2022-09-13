#inisialisasi objek flask
from distutils.log import debug
from flask import Flask

app = Flask(__name__)

#running app

if __name__ == '__main__':
    app.run(debug = True)

@app.get("/")
def index():
    return "hello world"

#import models dan routes
#from app import models, routes