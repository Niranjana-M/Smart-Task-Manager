from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# ---------------- MODELS ---------------- #

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.Date)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
login_manager.login_view = 'login'

# ---------------- AUTH ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'],
                                    password=request.form['password']).first()
        if user:
            login_user(user)
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ---------------- DASHBOARD ---------------- #

@app.route('/')
@login_required
def index():
    search = request.args.get('search')
    filter_type = request.args.get('filter')

    tasks = Task.query.filter_by(user_id=current_user.id)

    if search:
        tasks = tasks.filter(Task.title.contains(search))

    if filter_type == "completed":
        tasks = tasks.filter_by(is_completed=True)
    elif filter_type == "pending":
        tasks = tasks.filter_by(is_completed=False)
    elif filter_type == "high":
        tasks = tasks.filter_by(priority="High")

    tasks = tasks.all()

    total = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, is_completed=True).count()
    pending = total - completed

    return render_template("index.html", tasks=tasks,
                           total=total, completed=completed, pending=pending)

# ---------------- ADD TASK ---------------- #

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    priority = request.form['priority']
    due_date = datetime.strptime(request.form['due_date'], "%Y-%m-%d")

    task = Task(title=title,
                priority=priority,
                due_date=due_date,
                user_id=current_user.id)

    db.session.add(task)
    db.session.commit()
    return redirect('/')

# ---------------- COMPLETE TASK ---------------- #

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    task = Task.query.get(id)
    task.is_completed = not task.is_completed
    db.session.commit()
    return redirect('/')

# ---------------- DELETE TASK ---------------- #

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

# ---------------- EXPORT CSV ---------------- #

@app.route('/export')
@login_required
def export():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Title', 'Priority', 'Due Date', 'Completed'])

    for t in tasks:
        writer.writerow([t.title, t.priority, t.due_date, t.is_completed])

    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()),
                     download_name="tasks.csv",
                     as_attachment=True)

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)