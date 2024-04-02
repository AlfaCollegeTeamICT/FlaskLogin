import os
from flask                  import Flask, render_template, url_for, current_app, redirect
from flask_sqlalchemy       import SQLAlchemy
from flask_login            import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.sql         import func
from flask_wtf              import FlaskForm
from wtforms                import StringField, PasswordField, SubmitField
from wtforms.validators     import InputRequired, Length, ValidationError
from flask_bcrypt           import Bcrypt

# Create Flask Application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))  # Define the "basedir" variable
app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY']                = ''

# Database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create User Model
class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(15), unique=True, nullable=False)
    password    = db.Column(db.String(80), nullable=False)

# Create Form Classes
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    
    password = PasswordField('password', validators=[InputRequired(), Length(
        min=8, max=80)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')
    # Custom Validation
    def validate_username(self, username):
        existing_user = User.query.filter_by(   
            username=username.data).first()
        if existing_user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    
    password = PasswordField('password', validators=[InputRequired(), Length(
        min=8, max=80)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Login')

# Create Database
app.app_context().push()
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Run Application
if __name__ == '__main__':
    app.run(debug=True)