from biblioteca.streamlit.utils.utilidades import (
    email_valido,
    campo_vacio,
    normalizar_texto,
    filtrar_libros,
    validar_libro
)


def test_email_valido():
    assert email_valido("test@gmail.com") == True
    assert email_valido("testgmail.com") == False


def test_campo_vacio():
    assert campo_vacio("") == True
    assert campo_vacio("   ") == True
    assert campo_vacio("hola") == False


def test_normalizar_texto():
    assert normalizar_texto("  Hola ") == "hola"


def test_filtrar_libros_por_titulo():
    libros = [
        {"titulo": "1984", "autor": "George Orwell", "genero": "Distopía", "disponible": True},
        {"titulo": "Dune", "autor": "Frank Herbert", "genero": "Ciencia ficción", "disponible": True}
    ]

    resultado = filtrar_libros(libros, "1984")

    assert len(resultado) == 1


def test_validar_libro():
    assert validar_libro("1984", "George Orwell", "Distopía") == True
    assert validar_libro("", "George Orwell", "Distopía") == False

    from biblioteca.streamlit.utils.utilidades import limpiar_texto, validar_usuario

    def test_limpiar_texto():
        assert limpiar_texto("  hola  ") == "hola"

    def test_validar_usuario():
        assert validar_usuario("Alex", "alex@gmail.com") == True
        assert validar_usuario("", "alex@gmail.com") == False
        assert validar_usuario("Alex", "alexgmail.com") == False

    def test_filtrar_libros_sin_resultados():
        libros = [
            {"titulo": "1984", "autor": "George Orwell", "genero": "Distopía", "disponible": True}
        ]

        resultado = filtrar_libros(libros, "Dune")

        assert len(resultado) == 0