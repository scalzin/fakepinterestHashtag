# criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship('Post', backref='user', lazy = True)
    

class Post(database.Model):
    id= database.Column(database.Integer, primary_key = True)
    imagem = database.Column(database.String, default = 'default.png')
    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.utcnow())
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable = False)