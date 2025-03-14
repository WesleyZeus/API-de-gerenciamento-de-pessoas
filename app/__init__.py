import os
from flask import Flask
from flask_restx import Api
from app.extensions import db, ma, jwt
from app.config.swagger import init_swagger
from app.controllers.user_controller import user_controller
from app.controllers.protected_controller import protected_controller



def create_app():
    app = Flask(__name__)
    
    # Configurações do Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'wesley_silva')

    # Inicializa as extensões
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    
    # Inicializa o Swagger
    init_swagger(app)



    # Registra os Blueprints
    app.register_blueprint(user_controller, url_prefix='/users')
    app.register_blueprint(protected_controller, url_prefix='/protected')

    return app
