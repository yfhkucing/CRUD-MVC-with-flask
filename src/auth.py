#isinya api endpoint (?)
from flask import Blueprint,request

#endpoint register
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register_():
    return 'hello user'