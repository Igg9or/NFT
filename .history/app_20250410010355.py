from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_nft.db'
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    class_grade = db.Column(db.String(10))
    profile_pic = db.Column(db.String(200), default='default.png')

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    rarity = db.Column(db.String(20), nullable=False, default='common')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.relationship('User', backref='nfts')

# Создаем папки при первом запуске
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    db.drop_all()  # Удаляем все таблицы
    db.create_all()  # Создаем заново с новой структурой
    
    # Создаем администратора
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin',
            class_grade='staff',
            profile_pic='default.png'
        )
        db.session.add(admin)
        db.session.commit()

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        class_grade = request.form.get('class_grade', '')
        
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            password=password,
            role=role,
            class_grade=class_grade
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        
        flash('Неверные учетные данные', 'danger')
    
    return render_template('auth/login.html')

# Выход
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Главная страница
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    recent_nfts = NFT.query.order_by(NFT.date_created.desc()).limit(5).all()
    
    return render_template('dashboard/dashboard.html', 
                         user=user,
                         recent_nfts=recent_nfts)

# Создание NFT
@app.route('/create-nft', methods=['GET', 'POST'])
def create_nft():
    if 'user_id' not in session or session['role'] not in ['teacher', 'admin']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        rarity = request.form['rarity']
        owner_id = request.form['owner_id']


        
        if 'media' in request.files:  # Переименуйте поле с 'image' на 'media'
            media_file = request.files['media']
            if media_file.filename != '':
                # Определяем тип файла
                file_ext = media_file.filename.split('.')[-1].lower()
                media_type = '3d_model' if file_ext in ['glb', 'gltf', 'obj'] else 'image'
                
                # Сохраняем файл
                filename = f"{datetime.now().timestamp()}.{file_ext}"
                media_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                media_url = f"uploads/{filename}"
                
                new_nft = NFT(
                title=title,
                description=description,
                media_url=media_url,  # Используем media_url вместо image_url
                media_type=media_type,  # Добавляем тип медиа
                rarity=rarity,
                owner_id=owner_id if owner_id else session['user_id']  # Добавляем fallback на текущего пользователя
            )
                db.session.add(new_nft)
                db.session.commit()
                
                flash('NFT успешно создан!', 'success')
                return redirect(url_for('my_nfts'))
    
    students = User.query.filter_by(role='student').all()
    return render_template('dashboard/create_nft.html', students=students)

# Мои NFT
@app.route('/my-nfts')
def my_nfts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard/my_nfts.html', user=user)

# Рейтинги
@app.route('/ratings')
def ratings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Топ пользователей по количеству NFT
    top_users = db.session.query(
        User.username,
        User.class_grade,
        db.func.count(NFT.id).label('nft_count')
    ).join(NFT).group_by(User.id).order_by(db.desc('nft_count')).limit(10).all()
    
    # Топ классов
    top_classes = db.session.query(
        User.class_grade,
        db.func.count(NFT.id).label('nft_count')
    ).join(NFT).group_by(User.class_grade).order_by(db.desc('nft_count')).all()
    
    return render_template('dashboard/ratings.html', 
                         top_users=top_users,
                         top_classes=top_classes)


@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)