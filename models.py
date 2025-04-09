# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    class_grade = db.Column(db.String(10))
    profile_pic = db.Column(db.String(200), default='default.png')
    nfts = db.relationship('NFT', backref='owner', lazy=True)

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)
    rarity = db.Column(db.String(20), nullable=False, default='common')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)