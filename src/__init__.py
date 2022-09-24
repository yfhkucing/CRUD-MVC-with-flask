from distutils.log import debug
from flask import Flask
import os
from src.database import db
from . import auth
from flask_jwt_extended import JWTManager
#applicatin factory flask
#secret key ada di file .env
#setup virtual enviroment ada di .flaskenv biar ga usah setup ulang setiap buka terminal baru

def create_app(test_config= None):

    app = Flask(__name__, instance_relative_config=True)
    #register blueprint
    app.register_blueprint(auth.bluePrint_)
    #inisialisasi database
    db.app=app
    db.init_app(app)
    #inisialisasi JWT
    JWTManager(app)
        
    if test_config is None:
        app.config.from_mapping( 
            SECRET_KEY=os.environ.get("kucing"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
            )
    
    else:
        app.config.from_mapping(test_config)

    
    return app
