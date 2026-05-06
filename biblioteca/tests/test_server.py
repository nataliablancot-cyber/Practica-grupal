import os
import tempfile

import pytest
from fastapi import HTTPException

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

from biblioteca.fastapi.server import (
    LibroCreate,
    PrestamoNoPermitido,
    UsuarioCreate,
    crear_libro,
    crear_prestamo,
    crear_usuario,
    historial_prestamos,
    inicializar_base_de_datos,
    listar_libros,
    listar_prestamos,
    listar_usuarios,
)


def setup_module():
    inicializar_base_de_datos()


def test_listar_libros_carga_catalogo_inicial():
    libros = listar_libros()["libros"]

    assert len(libros) >= 5
    assert any(libro.titulo == "1984" for libro in libros)


def test_crear_libro():
    libro = crear_libro(
        LibroCreate(
            titulo="Refactoring",
            autor="Martin Fowler",
            genero="Tecnico",
            disponible=True,
        )
    )

    assert libro.id is not None
    assert libro.etiqueta == "Refactoring - Martin Fowler"


def test_crear_usuario_y_listar_usuarios():
    usuario = crear_usuario(
        UsuarioCreate(nombre="Ana", email="ana@example.com", activo=True)
    )
    usuarios = listar_usuarios()

    assert usuario.id is not None
    assert usuario.esta_activo is True
    assert any(item.email == "ana@example.com" for item in usuarios)


def test_no_permite_email_duplicado():
    with pytest.raises(HTTPException) as error:
        crear_usuario(UsuarioCreate(nombre="Ana", email="ana@example.com", activo=True))

    assert error.value.status_code == 400


def test_crear_prestamo_e_historial():
    usuario = crear_usuario(
        UsuarioCreate(nombre="Luis", email="luis@example.com", activo=True)
    )
    libro = next(libro for libro in listar_libros()["libros"] if libro.disponible)

    prestamo = crear_prestamo(libro_id=libro.id, usuario_id=usuario.id)
    historial = historial_prestamos(usuario_id=usuario.id)
    prestamos = listar_prestamos()

    assert prestamo.libro_id == libro.id
    assert historial["prestamos"][0].libro_id == libro.id
    assert any(item.id == prestamo.id for item in prestamos)


def test_no_presta_libro_no_disponible():
    usuario = crear_usuario(
        UsuarioCreate(nombre="Marta", email="marta@example.com", activo=True)
    )
    libro = next(libro for libro in listar_libros()["libros"] if not libro.disponible)

    with pytest.raises(HTTPException) as error:
        crear_prestamo(libro_id=libro.id, usuario_id=usuario.id)

    assert error.value.status_code == 400


def test_excepcion_personalizada():
    error = PrestamoNoPermitido("No permitido")

    assert error.status_code == 400
    assert error.detail == "No permitido"
