from db import *

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