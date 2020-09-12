from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'SECRET_KEY!'
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)