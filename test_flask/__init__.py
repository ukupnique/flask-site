from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from test_flask.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail
#import locale, sys

#if sys.platform == 'win32':
#    locale.setlocale(locale.LC_ALL, 'rus_rus')
#else:
#    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from test_flask.main.routes import main
    from test_flask.users.routes import users
    from test_flask.posts.routes import posts
    from test_flask.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    return app
