from distutils.log import debug
from flask import Flask
import os
from src.database import db
from . import auth

#applicatin factory flask
#secret key ada di file .env
#setup virtual enviroment ada di .flaskenv biar ga usah setup ulang setiap buka terminal baru

def create_app(test_config= None):

    app = Flask(__name__, instance_relative_config=True)
    
    #register blueprint
    
    app.register_blueprint(auth.bluePrint_)
    #return app
    # (general rule syntax : is None instead == None)
        
    if test_config is None:
        app.config.from_mapping( 
            SECRET_KEY=os.environ.get("kucing"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
            )
    
    else:
        app.config.from_mapping(test_config)

    #inisialisasi database?
    db.app=app
    db.init_app(app)
    
    return app
