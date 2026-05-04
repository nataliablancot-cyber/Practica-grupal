from sqlalchemy import Column, Integer, String, Boolean , Date
from database import Base
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    disponible = Column(Boolean, nullable=False)

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, autoincrement=True, primary_key=True)
    usuario_id = Column(String, nullable=False)
    libro_id = Column(Integer, nullable=False)
    fecha_prestamo = Column(Date, default=datetime.date.today)
    fecha_devolucion = Column(Date, nullable=True)
    estado = Column(String, default="Activo")

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    activo = Column(Boolean, default=True)

