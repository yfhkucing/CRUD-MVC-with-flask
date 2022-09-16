from flask import Flask
import os

#for configuration?

def create_app(test_config= None):

    app = Flask(__name__, instance_relative_config=True)

    # (general rule syntax : is None instead == None)
        
    if test_config is None:
        app.config.from_mapping( 
            SECRET_KEY='dev',
            )
    
    else:
        app.config.from_mapping(test_config)

    @app.get('/')

    def halo():
        return "hello world"

    return app
