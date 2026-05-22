from flask import render_template,request,redirect,url_for
from main import app
from db import *
from models.usuario_model import *

@app.route('/usuario/cadastro', methods=['GET'])
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('usuarios/cadastrar_usuario.html')

@app.route('/usuario/salvar',methods=['POST'])
def salvar_usuario():
    if request.method == 'POST':
        db = Session()
        nome = request.form.get('nome_usuario')
        email = request.form.get('email_usuario')
        departamento = request.form.get('departamento_usuario')
        ramal = request.form.get('ramal_usuario')
        senha = request.form.get('senha_usuario')
        senha_confirm = request.form.get('senha_usuario_confirm')
        status = request.form.get('status')
        if senha == senha_confirm:
            usuario = Usuario(
                nome=nome,
                email=email,
                departamento=departamento,
                ramal=ramal,
                senha=senha,
                status=status
            )
            db.add(usuario)
            db.commit()
            db.close()
            print('USUARIO CRIADO')
            return redirect(url_for('listar_usuario'))
        else:
            print('Senha diferentes')
            return redirect(url_for('cadastrar_usuario'))

@app.route('/usuario/listar')
def listar_usuario():
    db = Session()
    users = db.query(Usuario).all()
    return render_template('usuarios/listar_usuario.html',users=users)

@app.route('/usuario/permissoes')
def permissoes_usuario():
    return render_template('usuarios/permissoes_usuario.html')

@app.route('/usuario/historico')
def historico_usuario():
    return render_template('usuarios/historico_usuario.html')