from flask import Flask, render_template, flash, redirect, url_for
from app import routes
import app.forms
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user
# from forms import LoginFrom

app = Flask(__name__)
app.config["SECRET_KEY"] = '1234'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MOOIFICATIONS"] = False

app.app_context().push()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(120))
    time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


@app.route('/')
@app.route('/index/')
def index():
    user = {'username': 'Customer', 'age': '16'}
    posts = [{
        'author': {'username': 'Mikhail', 'age': '16'},
        'body': 'How are you?'

    },
        # {
        #     'author': {'username': 'Valyn', 'age': '16'},
        #     'body': 'Good!'
        #
        # }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)



def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('Login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sing In', form=form)



@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginFrom()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect('/')
    return render_template('login.html', title='Sign in', form=form)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    form = forms.PhoneFrom()
    return render_template('phone.html', title='Phone', form=form)


@app.route('/all', methods=['GET', 'POST'])
def all_user():
    user = {'username':'Misha', 'password': '1234', 'email': 'mido193@gmail.com'}
    return render_template('all.html', title='About User', user=user)


@app.route('/button2', methods=['GET', 'POST'])
def button2_user():
    user = 'button2.html'
    return render_template('button2.html', title='button2', user=user)


@app.route('/button1', methods=['GET', 'POST'])
def button1_user():
    user = 'button1.html'
    return render_template('button1.html', title='button1', user=user)