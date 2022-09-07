from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
from cryptography.fernet import Fernet
from flask_mail import Mail
import os

# Configuration de l'app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = os.environ.get('APP_KEY')
app.config['UPLOAD_FOLDER'] = 'home/static/files'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Configuration Email sur l'application
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USER'] = os.environ.get('MAIL_DEFAULT_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD_MAIL')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

#Configuration de la base de données et login
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view='log'
login_manager.login_message_category='info'
key = os.environ.get('SECRET_KEY')
fr = Fernet(key)


from home import roots
