API de Gerenciamento de Pessoas
Descrição
A API de Gerenciamento de Pessoas foi desenvolvida para permitir a gestão de usuários em um sistema, com funcionalidades como registro, login, edição, deleção e controle de permissões. A aplicação foi construída com Flask e utiliza SQLAlchemy como ORM para interagir com um banco de dados SQLite. A API segue a arquitetura RESTful e utiliza JWT (JSON Web Tokens) para autenticação, garantindo que apenas usuários autenticados possam acessar rotas protegidas e realizar ações sensíveis.

Este projeto é ideal para quem deseja aprender a implementar funcionalidades de controle de acesso e gerenciar usuários com autenticação e autorização via tokens JWT, além de ser uma ótima adição para portfólios de desenvolvedores back-end.

Funcionalidades
Registro de Usuários: Permite a criação de novos usuários no sistema, com atribuição de papéis como user ou admin.
Login de Usuários: Permite a autenticação de usuários e gera um token JWT para autorizar futuras requisições.
Edição de Usuários: Permite a edição das informações de um usuário, como username e password.
Deleção de Usuários: Permite a exclusão de um usuário do sistema.
Promoção de Usuários: Permite promover um usuário para o papel de administrador.
Autorização via JWT: Protege as rotas e garante que apenas usuários autenticados possam acessar os recursos restritos.
Tecnologias Utilizadas
Flask: Framework minimalista para web em Python, utilizado para a criação da API.
SQLAlchemy: ORM (Object-Relational Mapper) para gerenciar o banco de dados e interagir com as tabelas de forma simples e eficiente.
SQLite: Banco de dados relacional utilizado para persistência dos dados de forma local.
Flask-JWT-Extended: Extensão para autenticação JWT, facilitando a criação e verificação de tokens.
pytest: Framework de testes utilizado para garantir a qualidade do código e o bom funcionamento das rotas da API.
Endpoints da API


=-=-=-=-=-=-=-=-=-=-=-= COMO TESTAR A API =-=-=-=-=-=-=-=-=-=-=-=

1. Usando o Swagger
A API oferece uma interface Swagger para facilitar os testes interativos das rotas.

Rodar a aplicação:
Certifique-se de que a aplicação está em execução. Caso não tenha iniciado o servidor, execute:


flask run
Acessar o Swagger:
Abra seu navegador e acesse (http://127.0.0.1:5000/swagger) (ou a URL configurada para a interface Swagger).
Na interface, você poderá ver todas as rotas da API, com descrição de parâmetros, tipos de resposta e outros detalhes. Além disso, você pode testar as rotas diretamente, fazendo requisições interativas.


2. Usando o Postman:

Se preferir usar o Postman para testar a API, siga os passos abaixo:


Instalar o Postman:
Se você ainda não tem o Postman instalado, faça o download aqui.


Configurar o Postman:
Abra o Postman e configure as rotas de acordo com os exemplos no "Endpoints da API".


Lembre-se de incluir o token JWT nas requisições que exigem autenticação. Para adicionar o token:

No Postman, adicione um novo cabeçalho (header) com o nome Authorization e o valor Bearer <seu_token>, onde <seu_token> é o token retornado após o login.


Fazer Requisições:

Com o Postman configurado, basta executar as requisições. Você pode importar a coleção de testes para facilitar o processo ou criar as requisições manualmente, conforme as rotas e detalhes fornecidos na documentação.


Destaques:

Swagger permite que você interaja diretamente com a API através de uma interface gráfica, facilitando os testes e o entendimento das rotas.
Postman oferece uma maneira prática de testar as rotas, principalmente se você preferir fazer requisições manualmente ou importar uma coleção de requisições para testar a API.


Aqui estão os principais endpoints da API para gerenciar usuários:

1. Registro de Usuário
Método: POST
URL: /users/register
Corpo da Requisição:
json
{
    "username": "nome_usuario",
    "password": "senha_do_usuario",
    "role": "user"  // ou "admin" dependendo do tipo de usuário
}


Resposta (sucesso):
json
{
    "message": "Usuário registrado com sucesso",
    "id": 1
}


Descrição: Registra um novo usuário no sistema, atribuindo um papel de user ou admin.




2. Login de Usuário
Método: POST
URL: /users/login
Corpo da Requisição:
json

{
    "username": "nome_usuario",
    "password": "senha_do_usuario"
}


Resposta (sucesso):
{
    "access_token": "JWT_TOKEN"
}


Descrição: Realiza o login de um usuário e retorna um token JWT. Esse token deve ser utilizado nas requisições subsequentes.


3. Editar Usuário

Método: PUT
URL: /users/edit/{user_id}
Cabeçalhos:
Authorization: Bearer <JWT_TOKEN>
Corpo da Requisição:

{
    "username": "novo_nome_usuario",
    "password": "nova_senha"
}

Resposta (sucesso):

{
    "message": "Usuário atualizado com sucesso!"
}

Descrição: Permite editar as informações de um usuário existente. Para isso, o usuário deve fornecer um token JWT válido no cabeçalho da requisição.

4. Deletar Usuário
Método: DELETE
URL: /users/delete/{user_id}
Cabeçalhos:
Authorization: Bearer <JWT_TOKEN>

Resposta (sucesso):

{
    "message": "Usuário deletado com sucesso!"
}


Descrição: Deleta um usuário do sistema. Apenas usuários com o papel de admin podem deletar outros usuários.


5. Promover Usuário
Método: PUT
URL: /users/promote/{user_id}
Cabeçalhos:
Authorization: Bearer <JWT_TOKEN>
Resposta (sucesso):

{
    "message": "Usuário promovido para administrador com sucesso!"
}


Descrição: Promove um usuário comum para o papel de administrador. Apenas administradores podem realizar essa operação.
Como Rodar o Projeto


Passo 1: Clone o Repositório
Primeiro, clone o repositório para a sua máquina local:


git clone https://github.com/username/projeto-gerenciamento-pessoas.git
cd projeto-gerenciamento-pessoas


Passo 2: Crie e Ative um Ambiente Virtual
Crie um ambiente virtual para isolar as dependências:


python3 -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`


Passo 3: Instale as Dependências
Instale as dependências necessárias com o comando:


pip install -r requirements.txt
Passo 4: Inicie o Servidor
Para rodar a aplicação localmente, use:


python app.py
A API estará disponível em http://localhost:5000.

Como Testar
Os testes automatizados estão implementados utilizando o framework pytest. Para rodar os testes, siga os seguintes passos:

Passo 1: Instale o pytest
Se você ainda não tiver o pytest instalado, use o comando:


pip install pytest
Passo 2: Execute os Testes
Agora, basta rodar os testes com:


pytest

Os testes garantirão que todas as funcionalidades da API estão operando corretamente.

Contribuições
Contribuições são bem-vindas! Se você deseja ajudar a melhorar o projeto, siga esses passos:

Faça um fork do repositório.
Crie uma nova branch (git checkout -b feature-nome-da-feature).
Faça suas alterações e crie um commit com uma descrição clara.
Envie um pull request com suas alterações.

