from flask import render_template,request,redirect
from main import app
from db import *
from models.usuario_model import *

@app.route('/usuario/cadastro', methods=['GET'])
def cadastrar_usuario():
    session = Session()
    nome = request.form.get('nome_usuario')
    email = request.form.get('email_usuario')
    departamento = request.form.get('departamento_usuario')
    ramal = request.form.get('ramal_usuario')
    senha = request.form.get('senha_usuario')
    senha_confirm = request.form.get('senha_usuario_confirm')
    status = request.form.get('status')
    if senha == senha_confirm:
        print('Senhas iguais')
    else:
        print('Senha diferentes')
    return render_template('usuarios/cadastrar_usuario.html')

@app.route('/usuario/listar')
def listar_usuario():
    return render_template('usuarios/listar_usuario.html')

@app.route('/usuario/permissoes')
def permissoes_usuario():
    return render_template('usuarios/permissoes_usuario.html')

@app.route('/usuario/historico')
def historico_usuario():
    return render_template('usuarios/historico_usuario.html')