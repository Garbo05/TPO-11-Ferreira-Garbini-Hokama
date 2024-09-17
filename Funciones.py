# Se importa "random" para elegir al azar. Se importa "emoji" para darle una
# calidad mayor a la salida por consola. Por ultimo se importa colorama para
# agregar colores en consola
import random
import emoji
from colorama import Fore, Style, init

# Se inicializa colorama con la función donde los colores vuelven a su
# estado original luego de cada mensaje
init(autoreset=True)

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

# Leer palabras desde un archivo .txt
def cargar_palabras(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        # Leer todas las líneas y eliminar los saltos de línea
        palabras = [linea.strip() for linea in f.readlines()]
    return palabras

def validate_palabra(palabras, word):
    if word not in palabras:  # Cambiado '!=' por 'not in'
        print(f"La palabra '{word}' no está en la lista.")
        return False  # Retorna False si la palabra no está en la lista
    return True  # Retorna True si la palabra está en la lista

# Verifica que la palabra ingresada sea válida
# (solo letras y de longitud 5)
def validate_guess(word):
    while (
        word == "" or
        (word != "-1" and not word.isalpha()) or
        (word != "-1" and len(word) != 5)
    ):
        if word == "":
            word = input(
                "No se ingresó ninguna palabra. "
                "Ingrese una palabra: "
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

# ---- FUNCION MODO NORMAL ---- #
def play_game(LIST, ATTEMPTS):
    # Ejemplo de palabra
    palabra_ejemplo = (
        f"{Fore.YELLOW}B{Fore.RED}A{Fore.YELLOW}R{Fore.RED}"
        f"C{Fore.GREEN}O{Style.RESET_ALL}"
    )
    # Explicación del modo de juego
    print(
        f"\nEl juego consiste en adivinar una palabra de 5 letras, "
        "para ello cuentas con 6 intentos. \nDespués de cada "
        f"intento se te informará qué letras se encuentran en "
        f"la palabra.\nSi se encuentra alguna letra en la posición "
        f"correcta se marcará en color {Fore.GREEN}VERDE{Style.RESET_ALL}."
        f"\nLas que formen parte de la palabra, pero están en la "
        f"posición incorrecta, se mostrarán en color "
        f"{Fore.YELLOW}AMARILLO{Style.RESET_ALL}."
        f"\nLas que no estén dentro de la palabra se mostrarán en "
        f"color {Fore.RED}ROJO{Style.RESET_ALL}."
        f"\n\nPor ejemplo, si la palabra oculta fuera 'LIBRO' "
        f"y usted ingresará 'BARCO' "
        f"el resultado se vería así: "
        f"{palabra_ejemplo}"
        f"\n\n {Fore.RED}(Ingrese -1 para finalizar la partida.)"
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
        
        # Validar que la palabra esté en la lista de palabras posibles
        if not validate_palabra(LIST, palabra):
            continue  # Si la palabra no está en la lista, vuelve a pedir un intento
        
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
        
        # Marca las letras presentes en la palabra pero en posición incorrecta (amarillo)
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