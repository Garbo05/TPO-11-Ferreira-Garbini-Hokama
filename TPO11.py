import random
# Importar emoji para decorar el texto en consola
import emoji
# Importar Fore de colorama para colores en consola
from colorama import Fore, init
# Los colores vuelven a su estado original luego de cada mensaje.
init(autoreset=True)

# FUNCIONES


# Imprime una variable
def print_variables(a):
    print(a)

# Verifica que la palabra ingresada sea válida (solo letras y de longitud 5)


def validate_guess(word):
    while not word.isalpha():
        word = input("La palabra no puede contener números. ",
                    f"Ingrese una palabra válida: ")
    while word == "":
        word = input("No se ingresó ninguna palabra. Ingrese una palabra: ")
    while len(word) != 5:
        word = input("Longitud incorrecta. Ingrese una palabra de 5 letras: ")
    return word

# DICCIONARIO PARA ELIMINAR TILDES


diccionario_tildes = {
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U'
}

# Elimina los acentos de una palabra


def remove_accents(word):
    resultado = ""
    for letra in word:
        if letra in diccionario_tildes:
            resultado += diccionario_tildes[letra]
        else:
            resultado += letra
    return resultado

# ---- FUNCION MODO NORMAL ---- #


def play_game(LIST, ATTEMPTS):
    # Explicación del modo de juego
    print(f"El juego consiste en adivinar una palabra de 5 letras, para ello",
        " cuentas con 6 intentos. Después de cada intento se te informará",
        " qué letras se encuentran en la palabra y si se encuentran en",
        " la posición correcta en color VERDE, y cuáles forman parte de",
        " la palabra, pero están en \nla posición incorrecta en color",
        " AMARILLO\nIngrese -1 para finalizar la partida.")

    # Selecciona aleatoriamente una palabra secreta de la lista
    secret_word = random.choice(LIST)

    # Bucle principal para realizar intentos
    for intentos in range(1, ATTEMPTS + 1):
        palabra = input(f"\nINTENTO N°{intentos}: ")

        # Break para finalizar la partida antes de terminar los intentos
        if palabra == "-1":
            break

        # Validamos que la palabra ingresada cumpla con el estándar
        palabra = validate_guess(palabra)

        # Convertimos la palabra en mayúsculas y removemos los acentos
        palabra = palabra.upper()
        palabra = remove_accents(palabra)

        # Lista para almacenar el resultado coloreado de cada intento
        resultado = [''] * 5

        # Diccionario para evitar problemas de repetición de letras
        diccionario_secreto = {letra: secret_word.count(letra)
                                for letra in set(secret_word)}

        # Marca las letras correctas (en posición correcta - verde)
        for i in range(len(palabra)):
            if palabra[i] == secret_word[i]:  # Letra en la posición correcta
                resultado[i] = Fore.GREEN + palabra[i]
                diccionario_secreto[palabra[i]] -= 1  # Restar del diccionario

        # Marca las letras presentes en la palabra pero
        # en posición incorrecta (amarillo)
        for i in range(len(palabra)):
            if resultado[i] == '':
                if palabra[i] in secret_word and diccionario_secreto[palabra[i]] > 0:
                    resultado[i] = Fore.YELLOW + palabra[i]
                    diccionario_secreto[palabra[i]] -= 1
                else:  # Letra no está en la palabra (rojo)
                    resultado[i] = Fore.RED + palabra[i]

        # Imprimir el resultado del intento con los colores correspondientes
        for res in resultado:
            print(f"{res}", end=" ")
        print()

        # Si la palabra adivinada es correcta, se termina el juego
        if palabra == secret_word:
            print(f"\nLa palabra secreta era {palabra}. ¡Felicitaciones! "
                f"{emoji.emojize(':partying_face:')}")
            break

    # Si no se adivina la palabra después del número máximo de intentos
    if palabra == "-1":
        print("Partida finalizada.")
    elif palabra != secret_word:
        print(f"\nMala suerte, se agotaron tus {ATTEMPTS} intentos "
            f"{emoji.emojize(':clown_face:')}\nLa palabra secreta era "
            f"{secret_word}.")

# PROGRAMA PRINCIPAL
# Lista de palabras posibles (temporal; se reemplazará por archivo .txt)
LISTA_PALABRAS_POSIBLES = ["CARTA", "MANGO", "PERRO", "LUGAR", "SALTA",
                        "LLAMA", "PLUMA", "LIMON", "BOTAS", "TIGRE",
                        "RADIO", "BARCO", "LIBRO", "VERDE", "FLACO"]

# Número máximo de intentos
INTENTOS_MAXIMO = 6

# Mensaje de bienvenida
print(f"\n{emoji.emojize(':robot:')} BIENVENIDO A STRINGLE!"
        f"{emoji.emojize(':thinking_face:')}")
bandera = True

while bandera:
    modo_normal = play_game(LISTA_PALABRAS_POSIBLES, INTENTOS_MAXIMO)
    restart = input("\nLe gustaría volver a jugar? (Y/N): ")
    restart = restart.upper()

    while restart != "Y" and restart != "N":
        restart = input("\nValor ingresado no reconocido. "
                        "Le gustaría volver a jugar? (Y/N): ")
        restart = restart.upper()

    if restart == "Y":
        bandera = True
    else:
        bandera = False
        print(f"\nGracias por jugar! {emoji.emojize(':people_hugging:')}\n")
