#isinya api endpoint buat autentikasi user
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
#User itu class yg ada di database.py,dipanggil di sini. kalo ga percaya coba cek aja wkwkwk
from src.database import User,db
#inisiasi blueprint
bluePrint_ = Blueprint("bluePrint_", __name__, url_prefix="/api/v1/auth")

@bluePrint_.post('/login')
def login():
    email = request.json.get('email','')
    password = request.json.get('password','')

    user = User.query.filter_by(email=email).first()
    #checking if there is user trying to log in
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        #cek kalo passwordnya bener
        if is_pass_correct :
            #ini token buat login, pesannya terenkripsi
            #cuma bisa dibaca mesin
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                        'refresh': refresh,
                        'access': access,
                        'username': user.username,
                        'email': user.email
                }})
    #kalo password salah
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
        
#/api/v1/auth/register
@bluePrint_.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    #kondisi biar user ga asal masukin data
    if len(password)<=6 :
        return jsonify({'error':'password is to short'}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST
    #username harus pake alphanumeric dna ga boleh pake spasi 
    # (referensi alfanumerik : https://www.w3schools.com/python/ref_string_isalnum.asp)
    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    #about password hash : https://www.okta.com/blog/2019/03/what-are-salted-passwords-and-password-hashing/
    pwd_hash = generate_password_hash(password)
    #parameter dalam user bisa dilihat di database.py
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    #commit dulu biar ke ke save
    db.session.commit()

    return jsonify({
        'message':'user created',
        'user' : {'username':username, 'email':email }
    }),HTTP_201_CREATED    
    

