from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from database import SessionLocal, Base, engine
from models import Book, Loan, User
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
    model_config = ConfigDict(from_attributes=True)


class ListadoLibros(BaseModel):
    libros: list[LibroRead] = Field(default_factory=list)


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    activo: bool = True


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
        try:
            libros = db.query(Book).all()
            return {"libros": libros}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/libros/")
def crear_libro(libro: LibroCreate):
    with SessionLocal() as db:
        try:
            nuevo_libro = Book(
                titulo=libro.titulo,
                autor=libro.autor,
                genero=libro.genero,
                disponible=libro.disponible,
            )
            db.add(nuevo_libro)
            db.commit()
            db.refresh(nuevo_libro)
            return nuevo_libro

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/prestamos/")
def create_loan(libro_id: int, usuario_id: int):
    with SessionLocal() as db:
        try:
            usuario = db.query(User).filter(User.id == usuario_id).first()
            if not usuario:
                raise HTTPException(status_code=404, detail="Este usuario no existe")

            libro = db.query(Book).filter(Book.id == libro_id).first()

            if not libro:
                raise HTTPException(status_code=404, detail="Este libro no existe")

            if not libro.disponible:
                raise HTTPException(status_code=400, detail="Este libro no está disponible")

            libro.disponible = False
            nuevo_prestamo = Loan(
                usuario_id=str(usuario_id),
                libro_id=libro_id,
                fecha_prestamo=datetime.date.today(),
                estado="Activo",
            )
            db.add(nuevo_prestamo)
            db.commit()
            db.refresh(nuevo_prestamo)

            return {
                "message": "Préstamo creado correctamente",
                "prestamo_id": nuevo_prestamo.id,
                "libro": libro,
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/prestamos/historial")
def historial_prestamos(usuario_id: int):
    with SessionLocal() as db:
        usuario = db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Este usuario no existe")

        prestamos = db.query(Loan).filter(Loan.usuario_id == str(usuario_id)).all()

        resultado = []
        for prestamo in prestamos:
            libro = db.query(Book).filter(Book.id == prestamo.libro_id).first()
            resultado.append({
                "usuario_id": prestamo.usuario_id,
                "libro_id": prestamo.libro_id,
                "titulo": libro.titulo if libro else "Desconocido",
                "fecha_prestamo": prestamo.fecha_prestamo,
                "fecha_devolucion": prestamo.fecha_devolucion,
                "estado": prestamo.estado,
            })

        return {"prestamos": resultado}




