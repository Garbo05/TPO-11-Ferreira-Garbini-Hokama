"""
FALTA AGREGAR:
- lectura de un archivo .txt que funcione como word bank en lugar de leer de una lista
- verificar que la palabra que ingrese el usuario sea una palabra real (se encuentre en el word bank)
- convertir palabras con tilde a palabras sin tilde (por ejemplo "ÁRBOL" lo debe leer como "ARBOL")
"""

import random
import re
from colorama import Fore, init
init()

#FUNCIONES

def print_variables(a):
    print(a)

def verify_guess(word):
    while word.isalpha() == False:
        word = input("La palabra no puede contener números. Ingrese una palabra válida: ")
    while word == "":
        word = input("No se ingresó ninguna palabra. Ingrese una palabra: ")
    while len(word) != 5:
        word = input("Longitud incorrecta. Ingrese una palabra de 5 letras: ") 
    return word
    

#PROGRAMA PRINCIPAL

LISTA_PALABRAS_POSIBLES = ["ARBOL","AMIGO","CAJON","CLASE","BOTON"]
#print_variables(LISTA_PALABRAS_POSIBLES)
palabra_secreta = random.choice(LISTA_PALABRAS_POSIBLES)
#print_variables(palabra_secreta)
INTENTOS_MAXIMO = 6
#Inicializacion de la lista en la que se van a agregar las letras que se encuenten en la palabra  

print("\nBIENVENIDO A STRINGLE!\nEl juego consiste en adivinar una palabra de 5 letras, para ello cuentas con 6 intentos, despues de cada intento se te informará qué letras se encuentran en la palabra y si se encuentran en la posicion correcta, y cuáles forman parte de la palabra, pero estan en la posicion incorrecta")

for intentos in range (1, INTENTOS_MAXIMO+1):
    palabra = input(f"\nINTENTO N°{intentos}: ")
    palabra = verify_guess(palabra)
    palabra = palabra.upper()
    #print_variables(palabra)

    resultado = []

    for i in range(len(palabra)):

        if palabra[i]==palabra_secreta[i]:
            letra_verde = Fore.GREEN+palabra[i]+Fore.RESET
            resultado.append(letra_verde)

        elif (palabra[i] in palabra_secreta) and palabra[i] != palabra_secreta[i]:
            letra_amarilla = Fore.YELLOW+palabra[i]+Fore.RESET
            resultado.append(letra_amarilla)

        else:
            letra_blanca = Fore.WHITE+palabra[i]+Fore.RESET
            resultado.append(letra_blanca)
    
    for i in range(len(resultado)):
        print(f"{resultado[i]}",end=" ")

    print()
    
    if palabra==palabra_secreta:
        print(f"\nLa palabra secreta era {palabra}. Felicitaciones!")
        exit()

if palabra != palabra_secreta:
    print(f"\nMala suerte, se agotaron tus {INTENTOS_MAXIMO} intentos, la palabra secreta era {palabra_secreta}.")