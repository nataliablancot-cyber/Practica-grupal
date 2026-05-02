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

class LibroCreate(BaseModel):
    titulo: str
    autor: str
    genero: str
    disponible: bool

class LibroRead(LibroCreate):
    id: int
    class Config:
        from_Atributes = True

class ListadoLibros(BaseModel):
    libros: list[LibroRead] = Field(default_factory=list)

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="1.0.0",
)
@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate):
    with SessionLocal() as db:
        usuario_existente = db.query(User).filter(
            User.email == usuario.email
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese email"
            )

        nuevo_usuario = User(
            nombre=usuario.nombre,
            email=usuario.email,
            activo=usuario.activo,
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return nuevo_usuario

@app.get("/libros/")
def retrieve_data():
    with SessionLocal() as db:
        db = SessionLocal()
        libros = db.query(Book).filter(Book.id == libro_id).first()

        return {"libros": libros}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
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
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")






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

        except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    @app.get ("/prestamos/historial")
    def historial_prestamos(usuario_id: str):
        with SessionLocal() as db:
            prestamos = db.query(Loan).filter(Loan.usuario_id == usuario_id).all()
            if not prestamos:
                raise HTTPException(status_code=404, detail="Este usuario no existe")

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





