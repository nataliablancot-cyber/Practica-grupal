from biblioteca.streamlit.utils.utilidades import email_valido, campo_vacio, normalizar_texto

def test_email_valido():
    assert email_valido("test@gmail.com") == True
    assert email_valido("testgmail.com") == False


def test_campo_vacio():
    assert campo_vacio("") == True
    assert campo_vacio("   ") == True
    assert campo_vacio("hola") == False

def test_normalizar_texto():
    assert normalizar_texto("  Hola ") == "hola"