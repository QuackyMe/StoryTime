from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=1000)
# app.secret_key = 'SECRET_KEY!'
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
