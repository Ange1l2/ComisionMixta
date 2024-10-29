from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

# create the object's application (variables)
login_manager = LoginManager()  # for auth
db = SQLAlchemy()  # for DB consults
bcrypt = Bcrypt()  # for hash password encrypt
mail = Mail()  # for send emails


# init flask_app function
def init_app(app_settings):
    global bcrypt, db, mail, app
    # create app configuration settings and folder templates definition
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(app_settings)

    # init login manager sessions with the app configuration
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message = 'Por favor identificate para ingresar a la aplicación'
    login_manager.login_message_category = "danger"

    # init sqlalchemy, bcrypt and mail
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from src.core.views import core_bp
    app.register_blueprint(core_bp)
    from src.accounts.views import accounts_bp
    app.register_blueprint(accounts_bp)

    from src.accounts.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    return app
