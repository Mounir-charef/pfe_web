from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
from cryptography.fernet import Fernet
from flask_mail import Mail
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = 'home/static/files'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USER'] = os.environ.get('MAIL_DEFAULT_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD_MAIL')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view='log'
login_manager.login_message_category='info'
key = os.environ.get('APP_KEY')
fr = Fernet(key)
from home import roots
