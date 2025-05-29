from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_login import LoginManager

from dotenv import load_dotenv
import os


db=SQLAlchemy()
jwt=JWTManager()
mail=Mail()
cors = CORS()
login_manager=LoginManager()
def create_app():
    load_dotenv() #load .env variables
    
    app=Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view="auth.login" #if not logged in user tries to access a @login_req route, redirect here
    
    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
   
        
    # app.register_blueprint(home_bp)
    # app.register_blueprint(auth, url_prefix='/auth')
    from .routes import register_blueprints
    register_blueprints(app)

   
    
    return app

