from biblioteca.streamlit.utils.utilidades import (
    campo_vacio,
    conectar,
    email_valido,
    filtrar_libros,
    limpiar_texto,
    normalizar_texto,
    validar_libro,
    validar_usuario,
)


def test_conectar():
    assert conectar() is True


def test_limpiar_texto():
    assert limpiar_texto("  texto ") == "texto"


def test_email_valido():
    assert email_valido("test@gmail.com") is True
    assert email_valido("testgmail.com") is False


def test_campo_vacio():
    assert campo_vacio("") is True
    assert campo_vacio("   ") is True
    assert campo_vacio("hola") is False


def test_normalizar_texto():
    assert normalizar_texto("  Hola ") == "hola"


def test_filtrar_libros_por_titulo():
    libros = [
        {"titulo": "1984", "autor": "George Orwell", "genero": "Distopia", "disponible": True},
        {"titulo": "Dune", "autor": "Frank Herbert", "genero": "Ciencia ficcion", "disponible": True},
    ]

    resultado = filtrar_libros(libros, "1984")

    assert len(resultado) == 1


def test_validar_libro():
    assert validar_libro("1984", "George Orwell", "Distopia") is True
    assert validar_libro("", "George Orwell", "Distopia") is False
    assert validar_libro("1984", "", "Distopia") is False
    assert validar_libro("1984", "George Orwell", "") is False


def test_validar_usuario():
    assert validar_usuario("Ana", "ana@example.com") is True
    assert validar_usuario("", "ana@example.com") is False
    assert validar_usuario("Ana", "anaexample.com") is False
