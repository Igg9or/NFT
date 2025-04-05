from flask import Flask, render_template, request, redirect, url_for
from models import db, User, NFT

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_nft.db'
db.init_app(app)

# Создаем админа при первом запуске
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
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