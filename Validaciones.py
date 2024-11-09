def cargar_palabras(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        palabras = [linea.strip() for linea in f.readlines()]
    return palabras


def remove_accents(word):
    diccionario_tildes = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    return ''.join(diccionario_tildes.get(letra, letra) for letra in word)


def validate_guess(word):
    return len(word) == 5 and word.isalpha()


def validate_palabra(palabras, word):
    word = remove_accents(word)
    return word in palabras
