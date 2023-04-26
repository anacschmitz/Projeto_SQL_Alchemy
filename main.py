from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
database_url = 'mysql+pymysql://root:253028@localhost/locadora'


class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Filme [Título = {self.titulo}, Gênero = {self.genero}, Ano = {self.ano}]'


def create_database():
    engine = create_engine(database_url, echo=True)
    try:
        engine.connect()
    except Exception as e:
        if '1049' in str(e):
            engine = create_engine(database_url.rsplit('/', 1)[0], echo=True)
            conn = engine.connect()
            conn.execute('CREATE DATABASE locadora')
            conn.close()
            print('Banco locadora criado com sucesso!')
        else:
            raise e

create_database()

#Configurações

engine = create_engine(database_url, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    Base.metadata.create_all(engine)
    print('Tabela filme criada com sucesso!')


create_table()

data_insert = Filme(titulo = 'Mario Bross', ano = '2023', genero = 'Animação')
session.add(data_insert)
session.commit()

#Remoção do banco
session.query(Filme).filter(Filme.titulo == 'Batman').delete()
session.commit()

#Atualização de dados
session.query(Filme).filter(Filme.id == 3).update( {'titulo' : 'Mario Bross.'})
session.commit()

#Consulta de dado
data = session.query(Filme).all()

print(f'Filmes {data}')

session.close()


