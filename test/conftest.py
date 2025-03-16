import pytest
from app import create_app
from app.extensions import db
from flask_jwt_extended import create_access_token
from app.models.user import User
from werkzeug.security import generate_password_hash
import app

@pytest.fixture
def app():
    app = create_app()  # Sua função de criação do app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando banco em memória
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados para testes
    yield app
    with app.app_context():
        db.drop_all()  # Limpa após os testes

# Fixture para criar o cliente
@pytest.fixture
def client(app):
    return app.test_client()

        