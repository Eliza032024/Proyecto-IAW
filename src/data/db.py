import os
from src.models.vehiculo import Vehiculo
from sqlmodel import SQLModel, Session, create_engine

db_user: str = "quevedo"
db_password: str = "1234"
db_server: str = "fastapi-db"
db_port: int = 3306
db_name: str = "vehiculodb"
#montar cadena de conexion
DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
#conectando mediante una variable
engine =create_engine(os.getenv("db_url",DATABASE_URL), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Vehiculo(matricula="a12b", modelo="Mazda", km_totales=100))
        session.add(Vehiculo(matricula="c34d", modelo="Citroen", km_totales=300))
        session.add(Vehiculo(matricula="e56f", modelo="Toyota", km_totales=200))
        session.add(Vehiculo(matricula="g78h", modelo="BMW", km_totales=350))
        session.commit()
