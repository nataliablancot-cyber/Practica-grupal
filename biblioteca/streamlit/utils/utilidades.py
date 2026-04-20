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
