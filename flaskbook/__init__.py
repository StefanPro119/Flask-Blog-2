from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskbook.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  #sa ovim kazemo da kada ukucamo u browser '/profile' da nas odvede do login funkcije, odnosno login page
login_manager.login_message_category = 'info' # ovo sluzi da bi se drugacije prikazala poruka kada treba da se ulogujes direktno u browser da bi video 'profile' i ovaj info je iz bootstrap-a, poruka je (Please log in to access this page.)
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskbook.users.routes import users
    from flaskbook.posts.routes import posts
    from flaskbook.main.routes import main
    from flaskbook.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app