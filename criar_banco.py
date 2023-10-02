from fakepinterest import database, app
from fakepinterest.models import User, Post

with app.app_context():
    database.create_all()