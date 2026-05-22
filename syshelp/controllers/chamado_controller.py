from flask import render_template,request,redirect, url_for
from main import app
from db import *
from models.chamado_model import *
from models.usuario_model import *
from datetime import datetime

@app.route('/chamado/abrir-chamado', methods=['GET'])
def abrirChamado():
    session = Session()
    users = session.query(Usuario).all()
    return render_template('chamados/abrir_chamado.html',users=users)

@app.route('/chamado/salvar',methods=['POST'])
def salvar():
    session = Session()

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    status = request.form.get('status')
    prioridade = request.form.get('prioridade')
    categoria = request.form.get('categoria')
    tecnico = request.form.get('tecnico')

    #PEGANDO AS DATAS
    data_abertura_str = request.form.get('data_abertura')
    data_fechamento_str = request.form.get('data_fechamento')

    #CONVERTENDO
    data_abertura = None
    if data_abertura_str:
        data_abertura = datetime.strptime(data_abertura_str, "%Y-%m-%d")

    data_fechamento = None
    if data_fechamento_str:
        data_fechamento = datetime.strptime(data_fechamento_str, "%Y-%m-%d")

    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        status=status,
        prioridade=prioridade,
        categoria=categoria,
        data_abertura=data_abertura,
        data_fechamento=data_fechamento,
        id_usuario=tecnico
    )
    session.add(chamado)
    session.commit()
    return redirect(url_for('listarChamado'))

@app.route('/chamado/listar')
def listarChamado():
    db = Session()
    chamados = db.query(Chamado).all()
    return render_template('chamados/listar_chamado.html',chamados=chamados)

@app.route('/chamado/status')
def statusChamado():
    db = Session()
    chamados = db.query(Chamado).all()
    return render_template('chamados/status.html',chamados=chamados)

@app.route('/chamado/status/alterar/<int:id>', methods=['GET'])
def alterarChamado(id):
    db = Session()
    chamado = db.query(Chamado).filter_by(id=id).first()
    usuario = db.query(Usuario).all()
    return render_template('chamados/alterar_chamado.html',chamado=chamado, usuario=usuario)

@app.route('/chamado/status/salvar/<int:id>',methods=['POST'])
def salvarAlteracao(id):
    db = Session()
    chamado = db.query(Chamado).filter_by(id=id).first()
    chamado.titulo = request.form.get('titulo')
    chamado.descricao = request.form.get('descricao')
    chamado.status = request.form.get('status')
    chamado.prioridade = request.form.get('prioridade')
    chamado.categoria = request.form.get('categoria')
    chamado.id_usuario = request.form.get('tecnico')

    data_abertura_str = request.form.get('data_abertura')
    data_fechamento_str = request.form.get('data_fechamento')

    chamado.data_abertura = datetime.strptime(data_abertura_str, "%Y-%m-%d") if data_abertura_str else None
    chamado.data_fechamento = datetime.strptime(data_fechamento_str, "%Y-%m-%d") if data_fechamento_str else None

    db.commit()
    db.close()
    return redirect(url_for('listarChamado'))

@app.route('/chamado/status/deletar/<int:id>', methods=['POST'])
def deletarChamado(id):
    db = Session()
    
    chamado = db.query(Chamado).filter(Chamado.id == id).first()

    if not chamado:
        return "Chamado não encontrado", 404

    db.delete(chamado)
    db.commit()
    return redirect(url_for('statusChamado'))

@app.route('/chamado/historico')
def historicoChamado():
    db = Session()
    chamados = db.query(Chamado).filter(Chamado.data_fechamento != None and Chamado.status == 'fechado').all()
    return render_template('chamados/historico.html', chamados=chamados)
