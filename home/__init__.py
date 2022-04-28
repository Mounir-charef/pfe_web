from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
from cryptography.fernet import Fernet
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = 'home/static/files'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='log'
login_manager.login_message_category='info'
key = 'SJsdqHDZTsE2H6BEUDLm2PnFWXGst7sqQrj-_Ic3XHU='
fr = Fernet(key)
from home import roots
