from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import Annotated

from src.models.vehiculo import Vehiculo
from src.data.db import get_session, init_db

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield
SessionDep= Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

@app.get("/vehiculo", response_model=list[Vehiculo])
async def lista_vehiculo(session: SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all() 
    return vehiculos


@app.post("/vehiculo", response_model=Vehiculo)
async def nuevo_vehiculo(Vehiculo: Vehiculo, session: SessionDep):
    session.add(Vehiculo)
    session.commit()
    session.refresh(Vehiculo)
    return Vehiculo


@app.delete("/vehiculo/{Vehiculo}")
def borrar_vehiculo(Vehiculos: str, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, )
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="vehiculo no encontrada")
    session.delete(vehiculo_encontrado)
    session.commit()
    return {"mensaje": "vehiculo eliminado"}

@app.patch("/vehiculo/{Vehiculo_matricula}", response_model=Vehiculo)
def cambia_vehiculo(Vehiculo_matricula: str, vehiculo: Vehiculo, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, Vehiculo_matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="vehiculo no encontrado")
    serie_data = vehiculo.model_dump(exclude_unset=True)
    vehiculo_encontrado.sqlmodel_update(serie_data)
    session.add(vehiculo_encontrado)
    session.commit()
    session.refresh(vehiculo_encontrado)
    return vehiculo_encontrado

