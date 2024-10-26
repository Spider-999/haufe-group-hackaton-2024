from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    # app config
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'verysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


    # app blueprint
    from .pages import pages
    from .auth import auth
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    # database setup
    from .models import User, PartyPost, Participant, Comment
    db.init_app(app)
    create_database(app)
    

    # login manager config
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def login_user(user_id):
        return User.query.get(int(user_id))
        

    return app


def create_database(app):
    with app.app_context():
        db.create_all()