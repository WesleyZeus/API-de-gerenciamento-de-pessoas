# app/controllers/user_controller.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from app.config.swagger import user_namespace, user_model, login_model
from flask_restx import Resource

user_controller = Blueprint('user_controller', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Decorador para garantir que o usuário seja admin
def admin_required(f):
    @wraps(f)
    def decorated_functions(*args, **kwargs):

        claims = get_jwt_identity()

        user = User.query.get(claims)
        
        if not user:
            return {"error": "Usuário não encontrado!"}, 404

        if user.role != 'admin':
            return {"error": "Precisa da Autorização do Adminstrador!"}, 403
        
        return f(*args, **kwargs)
    return decorated_functions



# Rota para registrar um novo usuário
@user_namespace.route('/register')
class Register(Resource):
    @user_namespace.expect(user_model)  
    def post(self):
        data = user_namespace.payload  

        if not data:
            return {"error": "Payload ausente ou inválido"}, 400

        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if not username or not password:
            return {"error": "Username e password são obrigatórios"}, 400  

        # Verificando se o usuário já existe
        if User.query.filter_by(username=username).first():
            return {"error": "Username já existe"}, 400

        # Cria o novo usuário
        new_user = User(
            username=username,
            password=generate_password_hash(password),  # Criptografando a senha
            role=role
        )

        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Usuário registrado com sucesso"}, 201



# Rota para login de usuário
@user_namespace.route('/login')
class Login(Resource):
    @user_namespace.expect(login_model)
    def post(self):
        

        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return {"error": "Username and password are required"}, 400
        
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid credentials"}, 401

        
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role}  
        )
        

        return {"access_token": f"Bearer {access_token}"}, 200

# Rota para deletar um usuário
@user_namespace.route('/delete/<int:user_id>')
class DeleteUser(Resource):
    @jwt_required()  # Exige autenticação
    @admin_required  # Apenas admin pode acessar
    @user_namespace.doc(security="Bearer Auth")
    def delete(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 200

# Rota para obter todos os usuários
@user_namespace.route('/users')
class GetAllUsers(Resource):
    @jwt_required()  # Exige autenticação
    @admin_required  # Apenas admin pode acessar
    @user_namespace.doc(security="Bearer Auth")
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200

@user_namespace.route("/promote/<int:user_id>")
class PromoterUser(Resource):
    @jwt_required()
    @admin_required
    @user_namespace.doc(security="Bearer Auth")
    def put(self, user_id):
        user = User.query.get(user_id)


        if not user:
            return {"error":"Usuário não encontrado!"}, 404
        
        if user.role == "admin":
            return {"error":"Usuário ja é administrador!"}
        
        user.role = "admin"
        db.session.commit()


        return {"mensagem":"Usuário promovido a administrador com sucesso!"}
    


@user_namespace.route("/editar/<int:user_id>", methods=["PUT"])
class EditarUsuario(Resource):
    @jwt_required()  # Garantir que o usuário esteja autenticado
    @user_namespace.expect(user_model)  # Espera o formato de user_model
    @user_namespace.doc(security="Bearer Auth", consumes=["application/json"])  # Especifica que espera JSON
    def put(self, user_id):
        claims = get_jwt_identity()  # Obtém o ID do usuário autenticado
        user_edit = User.query.get(user_id)  # Busca o usuário no banco de dados

        if not user_edit:
            return {"message": "Usuário não encontrado!"}, 404

        # Verifica se o usuário está tentando editar a si mesmo ou é um administrador
        if user_edit.id != int(claims) and not User.query.get(claims).role == "admin":
            return {"error": "Você não tem permissão para editar esse usuário!"}, 403

        data = request.json  # Extrai os dados JSON da requisição
        username = data.get("username", user_edit.username)
        password = data.get("password", user_edit.password)
        role = data.get("role", user_edit.role)

        # Verifica se o username já existe
        if username != user_edit.username and User.query.filter_by(username=username).first():
            return {"error": "Username já existe!"}, 400

        # Atualiza os dados do usuário
        user_edit.username = username
        if password:  # Só atualiza a senha se um novo valor for fornecido
            user_edit.password = generate_password_hash(password)
        user_edit.role = role

        db.session.commit()

        return {"message": "Usuário atualizado com sucesso!"}, 200
