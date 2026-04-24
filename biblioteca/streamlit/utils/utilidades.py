def conectar ():
    return True
def limpiar_texto(texto):
    # Quitamos espacios al principio y al final
    texto = texto.strip()
    return texto


def campo_vacio(texto):
    # Comprobamos si está vacío o solo tiene espacios
    if texto == "":
        return True
    if texto.strip() == "":
        return True
    return False

# cambio para commit

def email_valido(email):
    # Esta función comprueba si un email tiene un formato básico válido
    # Comprobamos que tenga @ y punto
    if "@" in email and "." in email:
        return True  # si cumple, es válido
    # si no cumple, devolvemos False
    return False

def normalizar_texto(texto):
    #Convertimos el texto a minúsculas y quita espacios
    texto = texto.strip()   # Sim espacios
    texto = texto.lower()   # Pasamos a minúsculas
    return texto

def filtrar_libros(libros, busqueda):
    #Función para filtrar libros por título o autor
    resultado = []
    busqueda = normalizar_texto(busqueda)

    for libro in libros:
        titulo = normalizar_texto(libro.get("titulo", ""))
        autor = normalizar_texto(libro.get("autor", ""))

        #Comprobamos si coincide con título o autor
        if busqueda in titulo or busqueda in autor:
            resultado.append(libro)

    return resultado

def validar_libro(titulo, autor, genero):
    #Comprobamos que los campos no estén vacíos

    if campo_vacio(titulo):
        return False

    if campo_vacio(autor):
        return False

    if campo_vacio(genero):
        return False

    return True

def validar_usuario(nombre, email):
    # comprobamos que el nombre no esté vacío
    if campo_vacio(nombre):
        return False

    # comprobamos que el email sea válido
    if not email_valido(email):
        return False

    return True


from biblioteca.streamlit.utils.utilidades import filtrar_libros, validar_libro


def test_filtrar_libros_por_titulo():
    libros = [
        {"titulo": "1984", "autor": "George Orwell", "genero": "Distopía", "disponible": True},
        {"titulo": "Dune", "autor": "Frank Herbert", "genero": "Ciencia ficción", "disponible": True}
    ]

    resultado = filtrar_libros(libros, "1984")

    assert len(resultado) == 1
    assert resultado[0]["titulo"] == "1984"


def test_filtrar_libros_por_autor():
    libros = [
        {"titulo": "1984", "autor": "George Orwell", "genero": "Distopía", "disponible": True},
        {"titulo": "Dune", "autor": "Frank Herbert", "genero": "Ciencia ficción", "disponible": True}
    ]

    resultado = filtrar_libros(libros, "orwell")

    assert len(resultado) == 1
    assert resultado[0]["autor"] == "George Orwell"


def test_validar_libro():
    assert validar_libro("1984", "George Orwell", "Distopía") == True
    assert validar_libro("", "George Orwell", "Distopía") == False
    assert validar_libro("1984", "", "Distopía") == False
    assert validar_libro("1984", "George Orwell", "") == False

