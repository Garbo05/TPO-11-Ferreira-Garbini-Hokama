import random
import re

#FUNCIONES

def verify_guess(word):
    if word == "":
        word = input("Ingrese una palabra. ")
    elif len(word) != 5:
        word = input("Ingrese una palabra de 5 letras. ") 
    elif word.isdigit() == True:
        word = input("Ingrese una palabra válida. ")

#PROGRAMA PRINCIPAL

lista = ["arbol","amigo","cajon","clase","boton"]

print("BIENVENIDO A STRINGLE\nEl juego consiste en adivinar una palabra de 5 letras, para ello contas con 6 intentos, despues de cada intento se te informara que palabras se encuentran en la posicion correcta y cuales forman parte de la palabra, pero estan en la posicion incorrecta")
palabra = input(" ")

hola = verify_guess(palabra)