from db import *

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