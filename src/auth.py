#isinya api endpoint (?)
from flask import Blueprint
#endpoint register
#inisiasi blueprint
bluePrint_ = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@bluePrint_.post('/register')
def register():
    return "hello user"