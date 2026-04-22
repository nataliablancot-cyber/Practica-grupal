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

