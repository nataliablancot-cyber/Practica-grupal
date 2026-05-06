import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

try:
    from .database import Base
except ImportError:
    from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    disponible = Column(Boolean, nullable=False)

    @property
    def etiqueta(self):
        return f"{self.titulo} - {self.autor}"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, autoincrement=True, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    fecha_prestamo = Column(Date, default=datetime.date.today)
    fecha_devolucion = Column(Date, nullable=True)
    estado = Column(String, default="Activo")

    usuario = relationship("User")
    libro = relationship("Book")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    activo = Column(Boolean, default=True)

    @property
    def esta_activo(self):
        return bool(self.activo)
