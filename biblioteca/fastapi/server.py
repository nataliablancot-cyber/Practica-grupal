from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel as PydanticBaseModel
from database import SessionLocal, Base, engine
from models import Book, Loan
import datetime
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
    with SessionLocal() as db:
        db = SessionLocal()
        libros = db.query(Book).all()

        return {"libros": libros}
    except Exception as e:
        return {"error": str(e)}
@app.post("/libros/")
def crear_libro(libro: Libro):
    with SessionLocal() as db:
        nuevo_libro = Book(titulo=libro.titulo,
                           autor=libro.autor,
                           genero = libro.genero,
                           disponible=libro.disponible)
        db.add(nuevo_libro)
        db.commit()
        db.refresh(nuevo_libro)
        return nuevo_libro


    except Exception as e:
        return {"error": str(e)}





@app.post("/prestamos/")
def create_loan(libro_id: int, usuario_id: str):
    with SessionLocal() as db:
        libro= db.query(Book).filter(Book.id == libro_id).first()

        if not libro:
            raise HTTPException(status_code=404, detail="Este libro no existe")

        if not libro.disponible:
            raise HTTPException(status_code=400, detail="Este libro no está disponible")

        libro.disponible = False
        nuevo_prestamo = Loan(
            usuario_id =usuario_id,
            libro_id = libro_id,
            fecha_prestamo = datetime.date.today(),
            estado = "Activo"
    )
        db.add(nuevo_prestamo)
        db.commit()
        db.refresh(nuevo_prestamo)

        return {"message": "Préstamo creado correctamente",
                "libro": libro}

    @app.get ("/prestamos/historial")
    def historial_prestamos(usuario_id: str):
        with SessionLocal() as db:
            prestamos = db.query(Loan).filter(Loan.usuario_id == usuario_id).all()

            resultado = []
            for prestamo in prestamos:
                libro = db.query(Book).filter(Book.id == prestamo.libro_id).first()
                resultado.append({
                    "usuario_id": prestamo.usuario_id,
                    "libro_id": prestamo.libro_id,
                    "titulo": libro.titulo if libro else "Desconocido",
                    "fecha_prestamo": prestamo.fecha_prestamo,
                    "fecha_devolucion": prestamo.fecha_devolucion,
                    "estado": prestamo.estado
                })

            return {"prestamos": resultado}

    except Exception as e:
        return {"error": str(e)}

    # This is a stub for students to implement
    return {"message": "Préstamo creado (no realmente)", "libro_id": libro_id}


