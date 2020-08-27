from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment

app = Flask(__name__)
db = SQLAlchemy(app)
js = Bundle('scripts/activity.js', output='gen/activity.js')
assets = Environment(app)
assets.register('activity.js', js)

app.secret_key = 'SECRET_KEY!'
app.config.from_pyfile('config.py')
