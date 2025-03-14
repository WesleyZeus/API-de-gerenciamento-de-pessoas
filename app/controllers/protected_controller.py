from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask , jsonify, Blueprint
from flask_restx import Namespace, Resource

protected_controller = Blueprint('protected_controller', __name__)

user_namespace = Namespace('users', description="Operações relacionadas a usuários")

@user_namespace.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user_id = get_jwt_identity()
    return jsonify(logged_in_as=user_id),200