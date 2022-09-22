#setup database
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

#ini inisiasi ORM, pake SQLalchemy
#pelajarin lagi struktur database
db = SQLAlchemy()

#dalam database ada user dan bookmark
class User(db.Model):
    #property dari user
    id = db.Column(db.Integer, primary_key=True)
    #unique = true agar tidak ada username yg sama, nullable = false agar tidak bisa diisi kosong
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    #untuk backward relation dengan bookmark
    bookmarks = db.relationship('Bookmark', backref="user")

    #fungsi untuk representasi class User
    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    #fungsi untuk menghasilkan short url
    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    #fungsi untuk representasi class bookmark
    def __repr__(self) -> str:
        return 'Boomark>>> {self.url}'