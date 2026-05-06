import datetime
import logging
from contextlib import asynccontextmanager
from typing import Iterable

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field

try:
    from .database import Base, engine, get_db_session
    from .models import Book, Loan, User
except ImportError:
    from database import Base, engine, get_db_session
    from models import Book, Loan, User


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("biblioteca.api")


class BibliotecaError(Exception):
    status_code = 400
    detail = "Error en la biblioteca"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class RecursoNoEncontrado(BibliotecaError):
    status_code = 404


class RecursoDuplicado(BibliotecaError):
    status_code = 400


class PrestamoNoPermitido(BibliotecaError):
    status_code = 400


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class LibroCreate(BaseModel):
    titulo: str
    autor: str
    genero: str
    disponible: bool = True


class LibroRead(LibroCreate):
    id: int
    etiqueta: str


class ListadoLibros(BaseModel):
    libros: list[LibroRead] = Field(default_factory=list)


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    activo: bool = True


class UsuarioRead(UsuarioCreate):
    id: int
    esta_activo: bool


class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoRead(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    titulo: str
    usuario: str
    fecha_prestamo: datetime.date
    fecha_devolucion: datetime.date | None = None
    estado: str


def iter_libros_iniciales() -> Iterable[LibroCreate]:
    datos = (
        ("The Great Gatsby", "F. Scott Fitzgerald", "Clasico", True),
        ("1984", "George Orwell", "Distopia", True),
        ("Python Crash Course", "Eric Matthes", "Tecnico", True),
        ("Clean Code", "Robert C. Martin", "Tecnico", False),
        ("The Pragmatic Programmer", "Andrew Hunt", "Tecnico", True),
    )
    for titulo, autor, genero, disponible in datos:
        yield LibroCreate(
            titulo=titulo,
            autor=autor,
            genero=genero,
            disponible=disponible,
        )


def inicializar_base_de_datos():
    Base.metadata.create_all(bind=engine)
    with get_db_session() as db:
        if db.query(Book).count() == 0:
            logger.info("Cargando catalogo inicial de libros")
            for libro in iter_libros_iniciales():
                db.add(Book(**libro.model_dump()))
        else:
            logger.info("Catalogo existente detectado")


def convertir_prestamo(prestamo: Loan) -> PrestamoRead:
    return PrestamoRead(
        id=prestamo.id,
        usuario_id=prestamo.usuario_id,
        libro_id=prestamo.libro_id,
        titulo=prestamo.libro.titulo if prestamo.libro else "Desconocido",
        usuario=prestamo.usuario.nombre if prestamo.usuario else "Desconocido",
        fecha_prestamo=prestamo.fecha_prestamo,
        fecha_devolucion=prestamo.fecha_devolucion,
        estado=prestamo.estado,
    )


def manejar_error(error: BibliotecaError):
    logger.warning("%s", error.detail)
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_base_de_datos()
    yield


app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestion de bibliotecas.",
    version="1.0.0",
    lifespan=lifespan,
)

libros_router = APIRouter(prefix="/libros", tags=["libros"])
usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])
prestamos_router = APIRouter(prefix="/prestamos", tags=["prestamos"])


@usuarios_router.post("/", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate):
    try:
        with get_db_session() as db:
            usuario_existente = db.query(User).filter(User.email == usuario.email).first()
            if usuario_existente:
                raise RecursoDuplicado("Ya existe un usuario con ese email")

            nuevo_usuario = User(**usuario.model_dump())
            db.add(nuevo_usuario)
            db.flush()
            db.refresh(nuevo_usuario)
            logger.info("Usuario creado: %s", nuevo_usuario.email)
            return nuevo_usuario
    except BibliotecaError as error:
        manejar_error(error)
    except Exception as error:
        logger.error("Error creando usuario: %s", error)
        raise HTTPException(status_code=500, detail="Error interno")


@usuarios_router.get("/", response_model=list[UsuarioRead])
def listar_usuarios():
    with get_db_session() as db:
        return db.query(User).order_by(User.nombre).all()


@libros_router.get("/", response_model=ListadoLibros)
def listar_libros():
    with get_db_session() as db:
        libros = db.query(Book).order_by(Book.titulo).all()
        return {"libros": libros}


@libros_router.post("/", response_model=LibroRead)
def crear_libro(libro: LibroCreate):
    try:
        with get_db_session() as db:
            nuevo_libro = Book(**libro.model_dump())
            db.add(nuevo_libro)
            db.flush()
            db.refresh(nuevo_libro)
            logger.info("Libro creado: %s", nuevo_libro.etiqueta)
            return nuevo_libro
    except Exception as error:
        logger.error("Error creando libro: %s", error)
        raise HTTPException(status_code=500, detail="Error interno")


@prestamos_router.post("/", response_model=PrestamoRead)
def crear_prestamo(libro_id: int, usuario_id: int):
    try:
        with get_db_session() as db:
            usuario = db.query(User).filter(User.id == usuario_id).first()
            if not usuario:
                raise RecursoNoEncontrado("Este usuario no existe")
            if not usuario.esta_activo:
                raise PrestamoNoPermitido("Este usuario no esta activo")

            libro = db.query(Book).filter(Book.id == libro_id).first()
            if not libro:
                raise RecursoNoEncontrado("Este libro no existe")
            if not libro.disponible:
                raise PrestamoNoPermitido("Este libro no esta disponible")

            libro.disponible = False
            nuevo_prestamo = Loan(
                usuario_id=usuario_id,
                libro_id=libro_id,
                fecha_prestamo=datetime.date.today(),
                estado="Activo",
            )
            db.add(nuevo_prestamo)
            db.flush()
            db.refresh(nuevo_prestamo)
            logger.info("Prestamo creado: usuario=%s libro=%s", usuario_id, libro_id)
            return convertir_prestamo(nuevo_prestamo)
    except BibliotecaError as error:
        manejar_error(error)
    except Exception as error:
        logger.error("Error creando prestamo: %s", error)
        raise HTTPException(status_code=500, detail="Error interno")


@prestamos_router.get("/", response_model=list[PrestamoRead])
def listar_prestamos():
    with get_db_session() as db:
        prestamos = db.query(Loan).order_by(Loan.fecha_prestamo.desc(), Loan.id.desc()).all()
        return [convertir_prestamo(prestamo) for prestamo in prestamos]


@prestamos_router.get("/historial", response_model=dict[str, list[PrestamoRead]])
def historial_prestamos(usuario_id: int):
    try:
        with get_db_session() as db:
            usuario = db.query(User).filter(User.id == usuario_id).first()
            if not usuario:
                raise RecursoNoEncontrado("Este usuario no existe")

            prestamos = (
                db.query(Loan)
                .filter(Loan.usuario_id == usuario_id)
                .order_by(Loan.fecha_prestamo.desc(), Loan.id.desc())
                .all()
            )
            return {"prestamos": [convertir_prestamo(prestamo) for prestamo in prestamos]}
    except BibliotecaError as error:
        manejar_error(error)


app.include_router(libros_router)
app.include_router(usuarios_router)
app.include_router(prestamos_router)
