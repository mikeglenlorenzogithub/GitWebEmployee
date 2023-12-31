from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    # ===== MODELS(DATABASE) =====>
    app.config['SECRET_KEY'] = 'abcdfghi jklmnopq rstuvwxy'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialize the app with Flask-SQLAlchemy
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()
        print('Create Database!')
    
    from .models import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app