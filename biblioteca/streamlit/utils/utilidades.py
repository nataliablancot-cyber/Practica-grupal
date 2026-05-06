def conectar():
    return True


def limpiar_texto(texto):
    return texto.strip()


def campo_vacio(texto):
    return texto.strip() == ""


def email_valido(email):
    return "@" in email and "." in email


def normalizar_texto(texto):
    return texto.strip().lower()


def filtrar_libros(libros, busqueda):
    resultado = []
    busqueda = normalizar_texto(busqueda)

    for libro in libros:
        titulo = normalizar_texto(libro.get("titulo", ""))
        autor = normalizar_texto(libro.get("autor", ""))

        if busqueda in titulo or busqueda in autor:
            resultado.append(libro)

    return resultado


def validar_libro(titulo, autor, genero):
    if campo_vacio(titulo):
        return False

    if campo_vacio(autor):
        return False

    if campo_vacio(genero):
        return False

    return True


def validar_usuario(nombre, email):
    if campo_vacio(nombre):
        return False

    if not email_valido(email):
        return False

    return True
