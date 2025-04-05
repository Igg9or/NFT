from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))  # "student", "teacher", "admin"
    class_grade = db.Column(db.String(10))  # "10-A"
    profile_pic = db.Column(db.String(200))  # Ссылка на аватар

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    rarity = db.Column(db.String(20))  # "common", "rare", "legendary"
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime)