from fastapi import FastAPI
import pandas as pd
from typing import List
from pydantic import BaseModel as PydanticBaseModel
from database import SessionLocal, Base, engine
from models import Book
Base.metadata.create_all(bind=engine)

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool

class ListadoLibros(BaseModel):
    libros: List[Libro] = []

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="1.0.0",
)

@app.get("/libros/")
def retrieve_data():
    # EDUCATIONAL INEFFICIENCY: Reading CSV on every request
    # Students should optimize this by using a database or caching
    try:
        db = SessionLocal()
        libros = db.query(Book).all()
        db.close()
        return {"libros": libros}
    except Exception as e:
        return {"error": str(e)}
@app.post("/libros/")
def crear_libro(libro: Libro):
    try:
        db = SessionLocal()
        nuevo_libro = Book(titulo=libro.titulo,
                           autor=libro.autor,
                           genero = libro.genero,
                           disponible=libro.disponible)
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)
        db.close()

        return nuevo_libro
    except Exception as e:
        return {"error": str(e)}





@app.post("/prestamos/")
def create_loan(libro_id: int):
    try:
        db = SessionLocal()
        libro= db.query(Book).filter(Book.id == libro_id).first()

        if not libro:
            db.close()
            return {"error": "Este libro no existe"}

        if not libro.disponible:
            db.close()
            return {"error": "Este libro no está disponible"}

        libro.disponible = False
        db.commit()
        db.refresh(libro)
        db.close()

        return {"message": "Préstamo creado correctamente",
                "libro": libro}
    except Exception as e:
        return {"error": str(e)}

    # This is a stub for students to implement
    return {"message": "Préstamo creado (no realmente)", "libro_id": libro_id} #nvdhfhdf