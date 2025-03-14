from flask_restx import Api, fields
from app.config.user_namespace import user_namespace


# Definindo o modelo do Swagger para o usuário
user_model = user_namespace.model('User', {
    'username': fields.String(required=True, description="Nome de usuário"),
    'password': fields.String(required=True, description="Senha do usuário"),
    'role': fields.String(default='user', description="Papel do usuário (default: 'user')")
})

# Definindo o modelo do Swagger para login
login_model = user_namespace.model('Login', {
    'username': fields.String(required=True, description="Nome de usuário"),
    'password': fields.String(required=True, description="Senha")
})


def init_swagger(app):
    """Função para configurar o Swagger da aplicação."""
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Insira o token no formato: Bearer <TOKEN>"
        }
    }

    api = Api(
        app,
        title="User Management API",
        version="1.0",
        description="API para gerenciar usuários",
        doc="/swagger",
        authorizations=authorizations,
        security="Bearer Auth"  # Definindo que a API requer autenticação com Bearer Token
    )
    api.add_namespace(user_namespace, path='/users')

