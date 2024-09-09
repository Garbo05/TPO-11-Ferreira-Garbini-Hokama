import random
import re

# Importar colorama para colores en consola
from colorama import Fore, init 
init(autoreset=True) # Los colores vuelven a su estado original luego de cada mensaje.

# Importar emoji para decorar el texto en consola
import emoji

#DICCIONARIO PARA ELIMINAR TILDES
diccionario_tildes = {
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U'
}

#FUNCIONES

# Imprime una variable
def print_variables(a):
    print(a)

# Verifica que la palabra ingresada sea válida (solo letras y de longitud 5)
def validate_guess(word):
    while word.isalpha() == False:
        word = input("La palabra no puede contener números. Ingrese una palabra válida: ")
    while word == "":
        word = input("No se ingresó ninguna palabra. Ingrese una palabra: ")
    while len(word) != 5:
        word = input("Longitud incorrecta. Ingrese una palabra de 5 letras: ") 
    
    return word

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
def play_game(LIST,ATTEMPTS):

    # Explicación del modo de juego
    print("\nEl juego consiste en adivinar una palabra de 5 letras, para ello cuentas con 6 intentos, despues de cada intento se te informará qué letras se encuentran en la palabra y si se encuentran en la posicion correcta en color VERDE, y cuáles forman parte de la palabra, pero estan en la posicion incorrecta en color AMARILLO\nIngrese -1 para finalizar la partida.")
    # Selecciona aleatoriamente una palabra secreta de la lista
    secret_word = random.choice(LIST)

    # Bucle principal para realizar intentos
    for intentos in range(1,ATTEMPTS+1):
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
        diccionario_secreto = {letra: secret_word.count(letra) for letra in set(secret_word)}

        # Primera pasada: Marca las letras correctas (en posición correcta - verde)
        for i in range(len(palabra)):
            if palabra[i] == secret_word[i]:  # Letra en la posición correcta (verde)
                resultado[i] = Fore.GREEN + palabra[i]
                diccionario_secreto[palabra[i]] -= 1  # Restar del diccionario solo si es verde

        # Segunda pasada: Marca las letras presentes en la palabra pero en posición incorrecta (amarillo)
        for i in range(len(palabra)):
            if resultado[i] == '':  # Solo procesamos los espacios que no son verdes
                if palabra[i] in secret_word and diccionario_secreto[palabra[i]] > 0:  # Letra en la palabra pero en la posición incorrecta
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
            print(f"\nLa palabra secreta era {palabra}. ¡Felicitaciones! {emoji.emojize(":partying_face:")}")
            break
            

    # Si no se adivina la palabra después del número máximo de intentos, se termina el juego
    if palabra == "-1":
        print("Partida finalizada.")
    elif palabra != secret_word:
        print(f"\nMala suerte, se agotaron tus {ATTEMPTS} intentos {emoji.emojize(":clown_face:")}\nLa palabra secreta era {secret_word}.")



# PROGRAMA PRINCIPAL

# Lista de palabras posibles (temporal; se reemplazará por archivo .txt)
LISTA_PALABRAS_POSIBLES = ["CARTA","MANGO","PERRO","LUGAR","SALTA","LLAMA","PLUMA","LIMON","BOTAS","TIGRE","RADIO","BARCO","LIBRO","VERDE","FLACO"]

# Número máximo de intentos
INTENTOS_MAXIMO = 6

# Mensaje de bienvenida
print(f"\n{emoji.emojize(":robot:")} BIENVENIDO A STRINGLE!{emoji.emojize(":thinking_face:")}")

bandera = True
while bandera:
    modo_normal = play_game(LISTA_PALABRAS_POSIBLES, INTENTOS_MAXIMO)

    restart = input("\nLe gustaría volver a jugar? (Y/N): ")
    restart = restart.upper()
    while restart != "Y" and restart != "N":
        restart = input("\nValor ingresado no reconocido. Le gustaría volver a jugar? (Y/N): ")
        restart = restart.upper()

    if restart == "Y":
        bandera = True
    else:
        bandera = False
        print(f"\nGracias por jugar! {emoji.emojize(":people_hugging:")}\n")