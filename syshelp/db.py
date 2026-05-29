from sqlalchemy import create_engine,Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker,relationship

URI = 'mysql+pymysql://root:@localhost:3307/test'
engine = create_engine(URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()

