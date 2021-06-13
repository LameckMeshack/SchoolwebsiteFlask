from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SECRET_KEY']='QWERTYUIOASDFGHJKL'

db = SQLAlchemy(app)
bcrypt= Bcrypt(app)



from school2.admin import routes
from school2.units import routes
