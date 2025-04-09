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
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Замените image_url на media_url для поддержки разных типов файлов
    media_url = db.Column(db.String(200), nullable=False)  
    media_type = db.Column(db.String(20), nullable=False)  # 'image', '3d_model'
    rarity = db.Column(db.String(20), nullable=False, default='common')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)