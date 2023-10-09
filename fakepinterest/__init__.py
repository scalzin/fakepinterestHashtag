from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://banco_fakepinterest_kgwa_user:SbjmTUBjEN6wFjaTnwl255JOuQsi5Nnt@dpg-cki4h1uafg7c73elpjo0-a/banco_fakepinterest_kgwa"
app.config['SECRET_KEY'] = 'ae201be0f4bf54b1837088a1038ad4d8'
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from fakepinterest import routes