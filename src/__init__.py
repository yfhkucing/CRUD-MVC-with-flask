from distutils.log import debug
from flask import Flask
import os
from src.database import db

#applicatin factory flask
#secret key ada di file .env
#setup virtual enviroment ada di .flaskenv biar ga usat setup ulang setiap buka terminal baru

def create_app(test_config= None):

    app = Flask(__name__, instance_relative_config=True)

    # (general rule syntax : is None instead == None)
        
    if test_config is None:
        app.config.from_mapping( 
            SECRET_KEY=os.environ.get("kucing"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI")
            )
    
    else:
        app.config.from_mapping(test_config)

    #inisialisasi database?
    db.app=app
    db.init_app(app)
    return app

if __name__ == '__main__':
    app.run(debug = True)