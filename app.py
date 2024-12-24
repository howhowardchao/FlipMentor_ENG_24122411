from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, User, db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 請更改為安全的密鑰

# 初始化數據庫
init_db(app)

def create_admin():
    # 檢查是否已存在admin用戶
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password=generate_password_hash('flip888'),
            name='Administrator',
            role='admin',
            points=100
        )
        db.session.add(admin)
        db.session.commit()

# 創建管理員帳號
with app.app_context():
    create_admin()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        if not all([name, username, password]):
            flash('All fields are required')
            return render_template('register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
            
        user = User(
            username=username,
            password=generate_password_hash(password),
            name=name,
            role='user',
            points=100
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/admin')
def admin():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
        
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
        
    user = User.query.get(user_id)
    action = request.form.get('action')
    
    if action == 'role':
        new_role = request.form.get('role')
        user.role = new_role
    elif action == 'points':
        points = int(request.form.get('points'))
        user.points += points
        
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Password updated successfully')
            
    return render_template('account.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True) 