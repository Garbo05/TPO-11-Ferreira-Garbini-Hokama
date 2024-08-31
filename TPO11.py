import random
import re

#FUNCIONES

def verify_guess(word):
    while word.isalpha() == False:
            word = input("La palabra no puede contener numeros. Ingrese una palabra válida. ")
    while word == "":
        word = input("No se ingreso ninguna palabra. Ingrese una palabra. ")
    while len(word) != 5:
        word = input("Longitud incorrecta. Ingrese una palabra de 5 letras. ") 
    

#PROGRAMA PRINCIPAL

LISTA_PALABRAS_POSIBLES = ["arbol","amigo","cajon","clase","boton"]

palabra_secreta = LISTA_PALABRAS_POSIBLES[random.randint(0,len(LISTA_PALABRAS_POSIBLES))]
INTENTOS_MAXIMO = 6




print("BIENVENIDO A STRINGLE\nEl juego consiste en adivinar una palabra de 5 letras, para ello contas con 6 intentos, despues de cada intento se te informara que letras estan en la palabra y se encuentran en la posicion correcta y cuales forman parte de la palabra, pero estan en la posicion incorrecta")

for intentos in range (1, INTENTOS_MAXIMO+1):
    palabra = input(f"INTENTO N° {intentos}\nIngrese una palabra de 5 letras:  ")
    palabra.lower
    palabra = verify_guess(palabra)
    

print(palabra)