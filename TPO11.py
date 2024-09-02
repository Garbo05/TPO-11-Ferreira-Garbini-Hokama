"""
FALTA AGREGAR:
- lectura de un archivo .txt que funcione como word bank en lugar de leer de una lista
- verificar que la palabra que ingrese el usuario sea una palabra real (se encuentre en el word bank)
"""

import random
import re
# Importar colorama para colores en consola
from colorama import Fore, init 
init(autoreset=True) # Los colores vuelven a su estado original luego de cada mensaje.

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
def verify_guess(word):
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
    print("\nEl juego consiste en adivinar una palabra de 5 letras, para ello cuentas con 6 intentos, despues de cada intento se te informará qué letras se encuentran en la palabra y si se encuentran en la posicion correcta en color VERDE, y cuáles forman parte de la palabra, pero estan en la posicion incorrecta en color AMARILLO")
    # Selecciona aleatoriamente una palabra secreta de la lista
    secret_word = random.choice(LIST)

    # Bucle principal para realizar intentos
    for intentos in range(1,ATTEMPTS+1):
        palabra = input(f"\nINTENTO N°{intentos}: ")
        palabra = verify_guess(palabra)
        palabra = palabra.upper()
        palabra = remove_accents(palabra)

        resultado = [] # Lista para almacenar el resultado coloreado de cada intento

        # Verifica cada letra de la palabra del usuario comparándola con la palabra secreta
        for i in range(len(palabra)):
            if palabra[i]==secret_word[i]:  # Letra en la posición correcta (verde)
                letra_verde = Fore.GREEN+palabra[i]+Fore.RESET
                resultado.append(letra_verde)

            elif palabra[i] in secret_word and palabra[i] != secret_word[i]:  # Letra en la palabra, pero en posición incorrecta (amarillo)
                letra_amarilla = Fore.YELLOW+palabra[i]+Fore.RESET
                resultado.append(letra_amarilla)

            else:  # Letra no está en la palabra (blanco)
                letra_blanca = Fore.WHITE+palabra[i]+Fore.RESET
                resultado.append(letra_blanca)
    
        # Imprimir el resultado del intento con los colores q correspondan
        for i in range(len(resultado)):
            print(f"{resultado[i]}",end=" ")

        print()

        # Si la palabra adivinada es correcta se termina el juego
        if palabra==secret_word:
            print(f"\nLa palabra secreta era {palabra}. Felicitaciones!")
            break

    # Si no se adivina la palabra después del número máximo de intentos se termina el juego
    if palabra != secret_word:
        print(f"\nMala suerte, se agotaron tus {INTENTOS_MAXIMO} intentos, la palabra secreta era {secret_word}.")



#PROGRAMA PRINCIPAL

# Lista de palabras posibles (temporal; se reemplazará por archivo .txt)
# Inicializamos la lista en la que se van a agregar las letras que se encuenten en la palabra:
LISTA_PALABRAS_POSIBLES = ["CARTA","MANGO","PERRO","LUGAR","SALTA","LLAMA","PLUMA","LIMON","BOTAS","TIGRE","RADIO","BARCO","LIBRO","VERDE","FLACO"]

# Número máximo de intentos
INTENTOS_MAXIMO = 6

# Mensaje de bienvenida
print("\nBIENVENIDO A STRINGLE!")

bandera = True
while bandera:
    modo_normal = play_game(LISTA_PALABRAS_POSIBLES,INTENTOS_MAXIMO)

    restart = input("\nLe gustaría volver a jugar? (Y/N): ")
    restart = restart.upper()
    while restart != "Y" and restart != "N":
        restart = input("\nValor ingresado no reconocido. Le gustaría volver a jugar? (Y/N): ")
        restart.upper()

    if restart == "Y":
        bandera = True
    else:
        bandera = False
        print("\nGracias por jugar!\n")