# Se importa "random" para elegir al azar. Se importa "emoji" para darle una
# calidad mayor a la salida por consola. Por ultimo se importa colorama para
# agregar colores en consola
import random
import emoji
from colorama import Fore, Style, init
# Se inicializa colorama con la función donde los colores vuelven a su
# estado original luego de cada mensaje
init(autoreset=True)

# FUNCIONES


# Imprime una variable


def print_variables(a):
    print(a)


# Verifica que la palabra ingresada sea válida (solo letras y de longitud 5)


def validate_guess(word):
    while (
        word == "" or
        (word != "-1" and not word.isalpha()) or
        (word != "-1" and len(word) != 5)
    ):
        if word == "":
            word = input(
                "No se ingresó ninguna palabra. "
                " Ingrese una palabra: "
                )
        elif word == "-1":
            return word  # Retorna '-1' para finalizar
        elif not word.isalpha():
            word = input(
                "La palabra no puede contener números. "
                "Ingrese una palabra válida: "
                )
        elif len(word) != 5:
            word = input(
                "Longitud incorrecta. "
                "Ingrese una palabra de 5 letras: "
                )
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
    # Ejemplo de palabra
    palabra_ejemplo = (
    f"{Fore.YELLOW}B{Fore.RED}A{Fore.RED}R{Fore.RED}C{Fore.GREEN}O"
    )
    # Explicación del modo de juego
    print(
        f"\nEl juego consiste en adivinar una palabra de 5 letras, "
        "para ello cuentas con 6 intentos. \nDespués de cada intento se te "
        "informará qué letras se encuentran en la palabra.\nSi se encuentra alguna "
        f"letra en la posición correcta se marcará en color {Fore.GREEN}VERDE{Style.RESET_ALL}."
        "\nLas que formen parte de la palabra, pero están en la posición incorrecta, "
        f"se mostrarán en color {Fore.YELLOW}AMARILLO{Style.RESET_ALL}."
        f"\nLas que no estén dentro de la palabra se mostrarán en color {Fore.RED}ROJO{Style.RESET_ALL}."
        "\n\nPor ejemplo, si la palabra oculta fuera 'LIBRO' y usted ingresará 'BARCO' "
        "el resultado se vería así: "
        f"{palabra_ejemplo}"
        "\n\n(Ingrese -1 para finalizar la partida.)"
    )

    # Selecciona aleatoriamente una palabra secreta de la lista
    secret_word = random.choice(LIST)

    # Bucle principal para realizar intentos
    for intentos in range(1, ATTEMPTS + 1):
        palabra = input(f"\nINTENTO N°{intentos}: ")

        # Validamos que la palabra ingresada cumpla con el estándar
        palabra = validate_guess(palabra)

        # Break para finalizar la partida antes de terminar los intentos
        if palabra == "-1":
            print("Partida finalizada.")
            break

        # Convertimos la palabra en mayúsculas y removemos los acentos
        palabra = palabra.upper()
        palabra = remove_accents(palabra)

        # Lista para almacenar el resultado coloreado de cada intento
        resultado = [''] * 5

        # Diccionario para evitar problemas de repetición de letras
        diccionario_secreto = {
            letra: secret_word.count(letra)
            for letra in set(secret_word)
            }

        # Marca las letras correctas (en posición correcta - verde)
        for i in range(len(palabra)):
            if palabra[i] == secret_word[i]:  # Letra en la posición correcta
                resultado[i] = Fore.GREEN + palabra[i]
                diccionario_secreto[palabra[i]] -= 1  # Restar del diccionario

        # Marca las letras presentes en la palabra pero
        # en posición incorrecta (amarillo)
        for i in range(len(palabra)):
            if resultado[i] == '':
                if (
                    palabra[i] in secret_word and
                    diccionario_secreto[palabra[i]] > 0
                ):
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
            print(
                f"\nLa palabra secreta era {palabra}. ¡Felicitaciones! "
                f"{emoji.emojize(':partying_face:')}"
                )
            break

    # Si no se adivina la palabra después del número máximo de intentos
    if palabra != secret_word and palabra != "-1":
        print(
            f"\nMala suerte, se agotaron tus {ATTEMPTS} intentos "
            f"{emoji.emojize(':clown_face:')}\nLa palabra secreta era "
            f"{secret_word}."
            )