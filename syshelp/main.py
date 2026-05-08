from flask import Flask, render_template,request,redirect, url_for
from sqlalchemy import create_engine,Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
from datetime import datetime

URI = 'mysql+mysqlconnector://root:@localhost:3306/test'
engine = create_engine(URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()
class Chamado(Base):
    __tablename__ ='chamado'
    id = Column(Integer,unique=True, primary_key=True, autoincrement=True)
    titulo = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=False)
    data_abertura = Column(DateTime, nullable=False)
    data_fechamento = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False)
    prioridade = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="chamados")

    responsavel_tecnico = Column(String(50), nullable=True)

class Usuario(Base):
    __tablename__ ='usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)
    departamento = Column(String(50), nullable=False)
    ramal = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)

    chamados = relationship("Chamado", back_populates="usuario")

Base.metadata.create_all(engine)

app = Flask(__name__)

#login "auth"
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session = Session()
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = session.query(Usuario).filter_by(email=email).first()
        
        if user.email == email and user.senha == senha:
            return render_template('/index.html')
    return render_template('/login.html')

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('chamados/historico.html')


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)