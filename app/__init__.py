


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'login'
lm.init_app(app)
#Bootstrap(app)
db = SQLAlchemy(app)
from app import views, models



