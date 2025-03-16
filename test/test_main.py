from test.conftest import client, User

def test_register(client):
    """Teste para a rota de registro de usuario"""

    response = client.post('/users/register', json={
        "username":"testuser",
        "password":"testsenha",
        "role":"user"
    })

    assert response.status_code == 201
    assert response.json["message"] == "Usuário registrado com sucesso"

def test_login(client):
    """Teste para a rota de login de usuário"""

    response = client.post('/users/register', json={
        "username":"testuser",
        "password":"testsenha",
        "role":"user"
    })

    response = client.post('/users/login', json={
        "username":"testuser",
        "password":"testsenha"
    })


    assert response.status_code == 200
    assert "access_token" in response.json #vai ver se o token foi gerado

from test.conftest import client

def test_get_all_users(client):
    """Teste para a rota que obtem todos os usuarios"""

    # Registrar um usuário admin
    register_response = client.post('/users/register', json={
        "username": "adminuser",
        "password": "adminpassword",
        "role": "admin"
    })

    assert register_response.status_code == 201

    # Realizar o login para obter o token
    login_response = client.post('/users/login', json={
        "username": "adminuser",
        "password": "adminpassword"
    })

    assert login_response.status_code == 200
    assert login_response.is_json

    login_data = login_response.json
    assert "access_token" in login_data, f"Resposta: {login_data}"

    # Obter o token JWT
    token = login_data.get("access_token", None)
    
    
    headers = {"Authorization": f" {token}"}

    response = client.get('/users/users', headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json)


def test_edit_user(client):
    """Teste para a rota de editar um usuário"""

    response = client.post('/users/register', json={
        "username": "testeuser",
        "password": "testsenha",
        "role": "user"
    })
    assert response.status_code == 201

    # Realiza o login para obter o token
    login_response = client.post('/users/login', json={
        "username": "testeuser",
        "password": "testsenha"
    })
    token = login_response.json["access_token"]

    # Obtém o ID do usuário
    user_id = 1  # Supondo que o usuário tenha ID 1

    # Tenta editar o usuário
    response = client.put(f'/users/editar/{user_id}', json={
        "username": "novo_username",
        "password": "novasenha"
    }, headers={
        "Authorization": f" {token}"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Usuário atualizado com sucesso!"

def test_delete_user(client, app):
    """Teste para deletar um usuário"""
   
    # Cria um usuário admin
    response = client.post('/users/register', json={
        "username": "admin",
        "password": "adminpass",
        "role": "admin"
    })
    assert response.status_code == 201
    admin_user_id = response.json["id"]  # Renomeado para admin_user_id

    # Cria um usuário para ser deletado
    response = client.post('/users/register', json={
        "username": "usuario3",
        "password": "senha123",
        "role": "user"
    })
    assert response.status_code == 201
    user_to_delete_id = response.json["id"]  # Renomeado para user_to_delete_id

    # Realiza login para obter o token de um admin
    admin_response = client.post('/users/login', json={
        "username": "admin",
        "password": "adminpass"
    })
    
    # Verifique o conteúdo da resposta
    print(admin_response.json)  # Verifique a resposta da API para ver se "access_token" está presente
    
    # Se o login falhar, o código de status será 401 e não haverá "access_token"
    if admin_response.status_code != 200:
        print(f"Falha no login: {admin_response.json}")
        assert False, "Login de administrador falhou"
    
    # Extrai o token
    admin_token = admin_response.json["access_token"].split(" ")[1]

    # Tenta deletar o usuário
    response = client.delete(f'/users/delete/{user_to_delete_id}', headers={
        "Authorization": f"Bearer {admin_token}"
    })

    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

    # Verifica se o usuário foi deletado dentro do contexto da aplicação
    with app.app_context():
        deleted_user = User.query.get(user_to_delete_id)
        assert deleted_user is None


def test_promote_user(client, app):
    """Teste para promover um usuário para admin"""

    # Cria um usuário para ser promovido

    response = client.post('/users/register', json={
        "username": "admin",
        "password": "adminpass",
        "role": "admin"
    })
    assert response.status_code == 201
    user_id = response.json["id"]

    response = client.post('/users/register', json={
        "username": "usuario4",
        "password": "senha123",
        "role": "user"
    })
    assert response.status_code == 201
    user_id = response.json["id"]

    # Realiza login para obter o token de um admin
    admin_response = client.post('/users/login', json={
        "username": "admin",
        "password": "adminpass"
    })

    # Verifica se o login foi bem-sucedido
    if admin_response.status_code != 200:
        print(f"Falha no login: {admin_response.json}")
    assert admin_response.status_code == 200, "Login de administrador falhou"

    admin_token = admin_response.json["access_token"].split(" ")[1]  # Pegando o token sem 'Bearer'

    # Tenta promover o usuário para admin
    response = client.put(f'/users/promote/{user_id}', headers={
        "Authorization": f"Bearer {admin_token}"
    })

    assert response.status_code == 200
    assert response.json["message"] == "Usuário promovido a administrador com sucesso!"

    # Verifica se o usuário foi promovido para admin
    with app.app_context():
        promoted_user = User.query.get(user_id)
        assert promoted_user is not None
        assert promoted_user.role == "admin"
