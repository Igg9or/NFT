from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_nft.db'
app.config['SECRET_KEY'] = 'ваш_секретный_ключ'  # Для сессий Flask

db = SQLAlchemy(app)

# Модели лучше вынести в отдельный файл, но для простоты оставим здесь
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

# Создаем таблицы и админа
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),  # Теперь функция определена
            role="admin",
            class_grade="staff"
        )
        db.session.add(admin)
        db.session.commit()

@app.route("/")
def home():
    return render_template("dashboard/index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for("dashboard"))
    return render_template("auth/login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/index.html")

if __name__ == "__main__":
    app.run(debug=True)